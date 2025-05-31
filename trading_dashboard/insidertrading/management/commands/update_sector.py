import yfinance as yf
import time
from django.core.management.base import BaseCommand
from django.db.models import Q
from insidertrading.models import Stock

''' This script updates the sector information for stocks in the database.
    It fetches the sector data from Yahoo Finance and updates the Stock model.
'''
class Command(BaseCommand):
    help = "Update sector information for all stocks in the database"

    def handle(self, *args, **kwargs):
        update_stock_sectors()

def update_stock_sectors():
    """Update sector information for all stocks in the database"""
    
    stocks_without_sector = Stock.objects.all().filter(Q(sector='Unknown') | Q(sector__isnull=True) | Q(sector='')).order_by('ticker')
    
    total_stocks = stocks_without_sector.count()
    print(f"Found {total_stocks} stocks to update")
    
    updated_count = 0
    failed_count = 0
    
    # Process in batches to avoid overwhelming the API
    batch_size = 50
    
    for i, stock in enumerate(stocks_without_sector):
        try:
            print(f"Processing {i+1}/{total_stocks}: {stock.ticker}")
            
            # Get stock info from yfinance
            ticker = yf.Ticker(stock.ticker)
            info = ticker.info
            
            # Extract sector/industry information
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            
            # Update the stock
            stock.sector = sector if sector else 'Unknown'
            stock.industry = industry if industry else 'Unknown'
            stock.save()
            
            updated_count += 1
            print(f"✓ Updated {stock.ticker}: {sector}")
            
            # Rate limiting - yfinance recommends not hammering their API
            if (i + 1) % batch_size == 0:
                print(f"Processed {i+1} stocks, sleeping for 10 seconds...")
                time.sleep(10)
            else:
                time.sleep(0.7)  # Small delay between requests
                
        except Exception as e:
            failed_count += 1
            print(f"✗ Failed to update {stock.ticker}: {str(e)}")
            continue
    
    print(f"\nCompleted! Updated: {updated_count}, Failed: {failed_count}")
