from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from insidertrading.models import WatchedStock
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
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
                    if ws.notifications_enabled:
                        message_lines.append(f"{ws.stock.ticker}: Current ${ws.stock.current_price}")

                message_lines.append("\n")
                # Fetch news articles for the user's stocks
                articles = newsArticle.objects.filter(symbol__in=[ws.stock.ticker for ws in watched]).distinct().order_by('-published_at')[:5]
                if articles.exists():
                    message_lines.append("Latest News Articles:\n")
                    for article in articles:
                        message_lines.append(f"{article.title} - {article.published_at.strftime('%Y-%m-%d %H:%M')}\n{article.url}\n")

            elif frequency == 'weekly':
                message_lines.append("Your Weekly Stock Watchlist Update:\n")
                for ws in watched:
                    if ws.notifications_enabled:
                        message_lines.append(f"{ws.stock.ticker}: Current ${ws.stock.current_price}")

                message_lines.append("\n")
                # Fetch news articles for the user's stocks
                articles = newsArticle.objects.filter(symbol__in=[ws.stock.ticker for ws in watched]).distinct().order_by('-published_at')[:5]
                if articles.exists():
                    message_lines.append("Latest News Articles:\n")
                    for article in articles:
                        message_lines.append(f"{article.title} - {article.published_at.strftime('%Y-%m-%d %H:%M')}\n{article.url}\n")

            else:
                continue 

            watched_lines = [f"{ws.stock.ticker}: Current ${ws.stock.current_price}" for ws in watched if ws.notifications_enabled]
            tickers = list(set(ws.stock.ticker for ws in watched))
            articles = newsArticle.objects.filter(symbol__in=tickers).order_by('-published_at')

            # De-duplicate articles by URL
            seen_urls = set()
            unique_articles = []
            for article in articles:
                if article.url not in seen_urls:
                    seen_urls.add(article.url)
                    unique_articles.append(article)
                if len(unique_articles) == 5:
                    break

            article_lines = [f"{a.title} - {a.published_at.strftime('%Y-%m-%d %H:%M')}<br><a href='{a.url}'>{a.url}</a>" for a in unique_articles]

            # Render HTML content
            html_content = render_to_string('emails/digest_template.html', {
                'username': user.username,
                'frequency': frequency.capitalize(),
                'watched_lines': watched_lines,
                'article_lines': article_lines,
            })

            # Fallback plain-text version
            text_content = "\n".join(message_lines)

            # Create and send the email
            email = EmailMultiAlternatives(
                subject="Stock Alert Notification",
                body=text_content,
                from_email="tradingdashboardbot@gmail.com",
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

        self.stdout.write(self.style.SUCCESS("Notifications sent based on user preferences."))