from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from insidertrading.models import WatchedStock
from django.core.mail import send_mail
from insidertrading.models import Profile
from insidertrading.models import newsArticle

class Command(BaseCommand):
    help = "Send notifications to users based on their selected frequency or price triggers."

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            frequency = getattr(user.profile, "notification_frequency", None)
            if not frequency:
                continue

            watched = WatchedStock.objects.filter(watchlist__user=user)
            if not watched.exists():
                continue

            message_lines = []

            if frequency == 'daily':
                message_lines.append("Your Daily Stock Watchlist Update:\n")
                for ws in watched:
                    message_lines.append(f"{ws.stock.ticker}: Current ${ws.stock.current_price}")

            elif frequency == 'weekly':
                message_lines.append("Your Weekly Stock Watchlist Update:\n")
                for ws in watched:
                    message_lines.append(f"{ws.stock.ticker}: Current ${ws.stock.current_price}")

            else:
                continue  # Unrecognized frequency, skip user

            # Send email
            send_mail(
                subject="Stock Alert Notification",
                message="\n".join(message_lines),
                from_email="noreply@yourapp.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Notifications sent based on user preferences."))