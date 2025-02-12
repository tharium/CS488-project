from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf

def index(request):
    return render(request, 'index.html')

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

