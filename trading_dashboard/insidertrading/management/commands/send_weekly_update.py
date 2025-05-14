from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from insidertrading.models import WatchedStock
from django.core.mail import send_mail  

class Command(BaseCommand):
    help = "Send weekly notifications to users"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(profile__notification_frequency='weekly')
        for user in users:
            watched = WatchedStock.objects.filter(watchlist__user=user)

            stock_summary = "\n".join(
                [f"{ws.stock.ticker}: Current ${ws.stock.current_price}" for ws in watched]
            )

            send_mail(
                subject="Your Weekly Stock Watchlist Update",
                message=f"Here are your stock updates:\n\n{stock_summary}",
                from_email="noreply@yourapp.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Weekly notifications sent."))