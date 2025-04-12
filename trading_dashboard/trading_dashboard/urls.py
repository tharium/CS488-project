from django.contrib import admin
from django.urls import path, include
from insidertrading import views

"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Homepage
    path('', views.index, name='index'),

    # Fix: Correct API route for fetching stock prices
    path('api/stock/', views.get_stock_price, name='get_stock_price'),
    path('api/stock/history/', views.get_stock_history, name='get_stock_history'),

    # Fix: Correct API route for fetching stock history
    path('api/stock/history/', views.get_stock_history, name='get_stock_history'),

    # User Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Secure Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Include additional routes from the 'insidertrading' app
    path('insidertrading/', include('insidertrading.urls')),

    # add a stock to a watchlist
    path('watchlist/add/<str:stock_ticker>/', views.add_stock, name='add_stock'),

    path('register/', views.register_view, name='register'),

    path('watchlist/', views.view_watchlist, name='view_watchlist'),

    path('watchlist/remove/<str:stock_ticker>/', views.remove_stock, name='remove_stock'),

    path('highprice/add/<str:stock_ticker>/<str:amount>/', views.add_high_price, name='add_high_price'),
    
    path('lowprice/add/<str:stock_ticker>/<str:amount>/', views.add_low_price, name='add_low_price'),

    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),
]
