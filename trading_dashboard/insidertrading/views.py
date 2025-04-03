from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.core.signing import Signer, BadSignature
import yfinance as yf
import random

# Initialize a signer instance for generating tokens
signer = Signer()

# Store email verification codes temporarily
verification_codes = {}

# Registration View (Creates User and Sends Email)
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

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
        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)

        # Generate a verification token
        token = signer.sign(username)
        verification_link = request.build_absolute_uri(f'/verify-email/{token}/')

        # Send verification email
        send_mail(
            "Verify Your Email - Trading Dashboard",
            f"Hello {username},\n\nClick the link below to verify your email:\n{verification_link}\n\nThank you!",
            "no-reply@tradingdashboard.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "A verification email has been sent. Please check your email.")
        return redirect("login")

    return render(request, "register.html")

# Email Verification View
def verify_email(request, token):
    try:
        username = signer.unsign(token)
        user = User.objects.get(username=username)

        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, "Your email has been verified! You can now log in.")
        else:
            messages.info(request, "Your email is already verified.")

    except (BadSignature, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")

    return redirect("login")

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Hardcoded Test User (Bypasses Database)
        if username == "testuser" and password == "password":
            request.session["logged_in"] = True  # Simulate login
            messages.success(request, "Login successful!")
            return redirect("/dashboard/")  # Redirect to dashboard

        #  Normal Authentication (For Real Users)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to homepage after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/dashboard/")  # Redirect to dashboard
            else:
                messages.error(request, "Please verify your email before logging in.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")

# Dashboard View (Requires Login = locked)
def dashboard(request):
    return render(request, 'dashboard.html')
    if request.user.is_authenticated:
        return render(request, "dashboard.html")
    else:
        messages.error(request, "You must be logged in to access the dashboard.")
        return redirect("login")

def get_stock_price(request):
    """Handles API requests for fetching stock prices"""
    symbol = request.GET.get('symbol', '').upper().strip()  # Get stock symbol

    if not symbol:
        return JsonResponse({"error": "No stock symbol provided"}, status=400)

    try:
        stock = yf.Ticker(symbol)  # Fetch stock data from Yahoo Finance
        stock_info = stock.history(period="1d")  # Get the latest price

        if stock_info.empty:
            return JsonResponse({"error": "Invalid stock symbol"}, status=400)

        latest_price = stock_info['Close'].iloc[-1]  # Get the most recent closing price
        return JsonResponse({"symbol": symbol, "price": round(latest_price, 2)})  # Return JSON response

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
def index(request):
    return render(request, 'index.html')



