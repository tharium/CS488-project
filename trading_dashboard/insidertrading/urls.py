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
    path('edit_trigger/<str:ticker>/', views.edit_trigger, name='edit_trigger'),
    path('delete_trigger/<str:ticker>/', views.delete_trigger, name='delete_trigger'),
    path('add_trigger/', views.add_trigger, name='add_trigger'),
    path('add_holding/', views.add_holding, name='add_holding'),
    path('delete_holding/<str:ticker>/', views.delete_holding, name='delete_holding'),
    path('register/', views.register_view, name='register'),
    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("search-stock/", views.search_stock, name="search_stock"),
    path('update_account/', views.update_account, name='update_account'),
    path('remove_stock/<str:stock_ticker>/', views.remove_stock, name='remove_stock'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('share_watchlist/', views.share_watchlist, name='share_watchlist'),
    path('refresh-news/', views.refresh_news, name='refresh_news'),
    path('edit_notifications/', views.edit_notifications, name='edit_notifications'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('api/tickers/', views.api_tickers, name='api_tickers'),
]