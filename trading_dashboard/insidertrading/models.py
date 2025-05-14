from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

# Create your models here.
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    stocks = models.ManyToManyField('Stock', through='WatchedStock')

class WatchedStock(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    price_trigger = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # notify_on_price_cross = models.BooleanField(default=True)

    class Meta:
        unique_together = ('watchlist', 'stock')

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volume = models.IntegerField(default=0)
    high_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    low_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.ticker} - {self.company_name} - {self.sector}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=64, blank=True, null=True)
    notification_frequency = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('none', 'None')], default='daily')
    blocked_sources = JSONField(default=list, blank=True)
class newsArticle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'symbol')
        ordering = ['-published_at']