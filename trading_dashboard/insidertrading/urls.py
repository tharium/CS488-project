from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/stock/', views.get_stock_price, name='get_stock_price'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
]