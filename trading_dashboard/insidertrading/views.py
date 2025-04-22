from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Watchlist, Stock, Profile
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.core.signing import BadSignature, TimestampSigner
from .utils.news import get_stock_news
import secrets
import yfinance as yf

import logging
logger = logging.getLogger(__name__)


# Homepage View
def index(request):
    return render(request, 'index.html')
# Initialize a signer instance for generating tokens
signer = TimestampSigner()

# Store email verification codes temporarily
verification_codes = {}

# Registration View (Creates User and Sends Email)
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["confirm_password"]

        # Validate password match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if username/email is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect("register")

        # Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = False  # Set user as inactive until email is verified
        user.save()
        # Generate a verification token

        token = secrets.token_urlsafe(32)
        print(token)
        profile = Profile.objects.create(user=user, verification_code=token)
        profile.save()

        verification_link = request.build_absolute_uri(f'/verify-email/{token}/')

        # Send verification email
        send_mail(
            "Verify Your Email - Trading Dashboard",
            f"Hello {username},\n\nClick the link below to verify your email:\n{verification_link}\n\nThank you!",
            "tradingdashboardbot@gmail.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "A verification email has been sent. Please check your email.")
        return redirect("/")

    return render(request, "register.html")

# Email Verification View
def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_code=token)
        user = profile.user

        if not user.is_active:
            user.is_active = True
            user.save()
            profile.verfication_code = None
            profile.save()
            messages.success(request, "Your email has been verified! You can now log in.")
        else:
            messages.info(request, "Your email is already verified.")

    except (BadSignature, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")

    return redirect("login")

def get_stock_history(request):
    symbol = request.GET.get('symbol', '')
    period = request.GET.get('period', '')

    print(str(symbol) + " " + str(period))
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period=period)

        print(str(stock_info))
        if stock_info.empty:
            #logger.error(f"Invalid stock symbol: {symbol}")
            return JsonResponse({"error": "Invalid stock symbol"}, status=400)

        history_data = {
            "dates": stock_info.index.strftime('%Y-%m-%d').tolist(),
            "prices": stock_info['Close'].tolist()
        }

        print(str(history_data))
        return JsonResponse(history_data)

    except Exception as e:
        #logger.error(f"Error fetching stock history for {symbol}: {str(e)}")
        
        return JsonResponse({"error": str(e)}, status=500)


# Login View
def login_view(request):
    print("Login view called")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("user is not none")
            if user.is_active:
                login(request, user)
                return redirect("/") 
            else:
                print("user is not active, need to verify?")
                return render(request, 'login.html', {'error': 'Invalid Credentials'})
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    watchlist, _ = Watchlist.objects.get_or_create(user=request.user)
    user_stocks = watchlist.stocks.all()
    # update stock prices
    for stock in user_stocks:
        price_data = get_stock_price(stock.ticker)
        stock.current_price = price_data["price"]
        stock.volume = price_data["volume"]
        stock.high_price = price_data["high"]
        stock.low_price = price_data["low"]
        stock.save()

    all_news = []
    for stock in user_stocks:
        news_articles = get_stock_news(stock.ticker, limit=1)  # get 1 article per stock
        for article in news_articles:
            all_news.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "published_at": article["publishedAt"],
                "source": article["source"]["name"],
            })

    # Optionally sort by published date
    all_news.sort(key=lambda x: x["published_at"], reverse=True)

    context = {
        "stocks": user_stocks,
        "news_articles": all_news[:5],  # limit total on dashboard to top 5
    }
            
    return render(request, "dashboard.html", context)

@login_required
def search_stock(request):
    print("search_stock view called")
    query = request.GET.get('q', '').strip()
    searched_stock = None
    in_watchlist = False

    if query:
        try:
            searched_stock = Stock.objects.get(
                Q(ticker__iexact=query) | Q(company_name__icontains=query)
            )
            watchlist = Watchlist.objects.get(user=request.user)
            in_watchlist = searched_stock in watchlist.stocks.all()
        except Stock.DoesNotExist:
            searched_stock = None

    context = {
        'search_query': query,
        'searched_stock': searched_stock,
        'in_watchlist': in_watchlist,
    }

    return render(request, 'partials/search_result.html', context)

def get_stock_price(symbol):
    """returns stock price data as a dict"""
    if not symbol:
        return {"error": "No stock symbol provided"}

    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        print(str(stock_info))

        if stock_info.empty:
            return {"error": "Invalid stock symbol"}

        latest_price = stock_info['Close'].iloc[-1]
        high = stock_info['High'].iloc[-1]
        low = stock_info['Low'].iloc[-1]
        volume = stock_info['Volume'].iloc[-1]
        return {
            "symbol": symbol,
            "price": round(latest_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "volume": volume
        }

    except Exception as e:
        return {"error": str(e)}

# def get_stock_history(request):
#     symbol = request.GET.get('symbol', '')
#     period = request.GET.get('period', '')

#     print(str(symbol) + " " + str(period))
#     try:
#         stock = yf.Ticker(symbol)
#         stock_info = stock.history(period=period)

#         print(str(stock_info))
#         if stock_info.empty:
            
#             return JsonResponse({"error": "Invalid stock symbol"}, status=400)

#         history_data = {
#             "dates": stock_info.index.strftime('%Y-%m-%d').tolist(),
#             "prices": stock_info['Close'].tolist()
#         }

#         print(str(history_data))
#         return JsonResponse(history_data)

#     except Exception as e:
        
#         return JsonResponse({"error": str(e)}, status=500)
def index(request):
    return render(request, 'index.html')

@login_required
def add_stock(request, stock_ticker):
    if request.method == "POST":
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        stock = get_object_or_404(Stock, ticker=stock_ticker)

        if stock in watchlist.stocks.all():
        
            messages.error(request, "Stock is already in your watchlist.")
        else:
            watchlist.stocks.add(stock)
            watchlist.save()
            messages.success(request, f"Added {stock.ticker} to your watchlist!")

        return redirect('dashboard')

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def remove_stock(request, stock_ticker):
    if request.method == "POST":
        watchlist = Watchlist.objects.get(user=request.user)
        stock = get_object_or_404(Stock, ticker=stock_ticker)

        if stock in watchlist.stocks.all():
            watchlist.stocks.remove(stock)
            watchlist.save()
            messages.success(request, f"Removed {stock.ticker} from your watchlist!")
        else:
            messages.error(request, "Stock not found in your watchlist.")

        # Redirect back to the watchlist page
        return redirect('view_watchlist')

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def view_watchlist(request):
    search_query = request.GET.get('q', '')
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    stocks_in_watchlist = watchlist.stocks.all()

    searched_stock = None
    if search_query:
        try:
            searched_stock = Stock.objects.get(
                Q(ticker__iexact=search_query) | Q(company_name__icontains=search_query)
            )
        except Stock.DoesNotExist:
            searched_stock = None

    return render(
        request,
        'dashboard.html',
        {
            'stocks': stocks_in_watchlist,
            'search_query': search_query,
            'searched_stock': searched_stock,
        },
    )

@login_required
def add_low_price(request, stock_ticker, amount):
    if request.method == "POST":
        watchlist = Watchlist.objects.get(user=request.user)
        stock = get_object_or_404(Stock, ticker=stock_ticker)

        if amount:
            watchlist.low_price = amount
            watchlist.save()
            messages.success(request, f"Set low price for {stock.ticker} to {amount}!")
        else:
            messages.error(request, "Invalid low price.")

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def add_high_price(request, stock_ticker, amount):
    if request.method == "POST":
        watchlist = Watchlist.objects.get(user=request.user)
        stock = get_object_or_404(Stock, ticker=stock_ticker)

        if amount:
            watchlist.high_price = amount
            watchlist.save()
            messages.success(request, f"Set high price for {stock.ticker} to {amount}!")
        else:
            messages.error(request, "Invalid high price.")

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=405)
