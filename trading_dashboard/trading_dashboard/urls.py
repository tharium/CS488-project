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

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Include additional routes from the 'insidertrading' app
    path('insidertrading/', include('insidertrading.urls')),

    # add a stock to a watchlist
    path('watchlist/add/<str:stock_ticker>/', views.add_stock, name='add_stock'),

    path('register/', views.register_view, name='register'),

    path('watchlist/', views.view_watchlist, name='view_watchlist'),

    path('watchlist/remove/<str:stock_ticker>/', views.remove_stock, name='remove_stock'),

    path('edit_trigger/<str:ticker>/', views.edit_trigger, name='edit_trigger'),

    path('delete_trigger/<str:ticker>/', views.delete_trigger, name='delete_trigger'),

    path('add_trigger/', views.add_trigger, name='add_trigger'),

    path('add_holding/', views.add_holding, name='add_holding'),

    path('delete_holding/<str:ticker>/', views.delete_holding, name='delete_holding'),

    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),

    path("search-stock/", views.search_stock, name="search_stock"),

    path('remove_stock/<str:stock_ticker>/', views.remove_stock, name='remove_stock'),

    path('add_stock/', views.add_stock, name='add_stock'),

    path('update_account/', views.update_account, name='update_account'),

    path('share_watchlist/', views.share_watchlist, name='share_watchlist'),

    path('refresh-news/', views.refresh_news, name='refresh_news'),

    path('edit_notifications/', views.edit_notifications, name='edit_notifications'),

    path('delete_account/', views.delete_account, name='delete_account')
]
