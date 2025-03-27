from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stocks = models.ManyToManyField('Stock', blank=True)
    low_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    high_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ticker} - {self.company_name} - {self.sector}"