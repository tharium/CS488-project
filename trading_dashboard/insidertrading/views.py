from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Watchlist, Stock
from django.shortcuts import get_object_or_404
import yfinance as yf

import logging
logger = logging.getLogger(__name__)


# Homepage View
def index(request):
    return render(request, 'index.html')

# Stock Price API View
def get_stock_price(request):
    symbol = request.GET.get('symbol', '')
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")

        if stock_info.empty:
            return JsonResponse({"error": "Invalid stock symbol"}, status=400)

        latest_price = stock_info['Close'].iloc[-1]
        return JsonResponse({"symbol": symbol, "price": latest_price})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to homepage after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('/')

# Dashboard View (Requires Login)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'register.html')

        # Create and save the user
        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # Log in the user immediately after registration
        return redirect('/')  # Redirect to homepage or dashboard

    return render(request, 'register.html')

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

        return redirect('view_watchlist')

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
        'watchlist.html',
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
