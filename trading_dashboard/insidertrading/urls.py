from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/stock/', views.get_stock_price, name='get_stock_price'),
]