from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stocks = models.ManyToManyField('Stock', blank=True)

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.ticker
