import time
import yfinance as yf
from django.core.management.base import BaseCommand
from insidertrading.models import Stock


'''
This script is for fetching stock tickers from a file and saving them to the database
Stores company name and ticker
Only run if the database is empty
This script is intended to be run as a Django management command.
'''

class Command(BaseCommand):
    help = "Fetch stock tickers and save them to the database"

    def handle(self, *args, **kwargs):
        # Load tickers from file
        with open("all_tickers.txt", "r") as f:
            tickers = [line.strip() for line in f.readlines()]

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                name = stock.info.get("longName", "Unknown Company")  # Get company name

                obj, created = Stock.objects.update_or_create(
                    ticker=ticker,
                    defaults={"company_name": name}
                )

                status = "Added" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(f"{status}: {ticker} - {name}"))

                time.sleep(0.9)  # Sleep to avoid hitting API rate limits

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error fetching {ticker}: {e}"))

        self.stdout.write(self.style.SUCCESS("Stock ticker update complete!"))