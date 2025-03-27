from django.urls import path
from . import views

app_name = 'insidertrading'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/stock/', views.get_stock_price, name='get_stock_price'),
    path('api/stock/history/', views.get_stock_history, name='get_stock_history'),
    path('watchlist/add/<str:stock_ticker>/', views.add_stock, name='add_stock'),
    path('watchlist/', views.view_watchlist, name='view_watchlist'),
    path('watchlist/remove/<str:stock_ticker>/', views.remove_stock, name='remove_stock'),
    path('highprice/add/<str:stock_ticker>/<str:amount>/', views.add_high_price, name='add_high_price'),
    path('lowprice/add/<str:stock_ticker>/<str:amount>/', views.add_low_price, name='add_low_price'),
]