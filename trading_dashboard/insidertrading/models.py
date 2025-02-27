from django.db import models
from django.contrib.auth.models import User

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stocks = models.ManyToManyField('Stock', blank=True)

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255) 
    sector = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} - {self.company_name}"
