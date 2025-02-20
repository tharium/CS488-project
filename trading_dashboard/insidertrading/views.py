from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import yfinance as yf

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


