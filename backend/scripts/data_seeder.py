from django.core.management.base import BaseCommand
from backend.trades.models import Trade
from backend.portfolios.models import Portfolio

class Command(BaseCommand):
    help = 'Seeds initial data into the database'

    def handle(self, *args, **kwargs):
        # Create sample portfolios
        portfolio1 = Portfolio.objects.create(name='Retirement Fund', description='Long-term investment portfolio')
        portfolio2 = Portfolio.objects.create(name='Emergency Fund', description='Short-term savings for emergencies')

        # Create sample trades
        Trade.objects.create(portfolio=portfolio1, symbol='AAPL', quantity=10, price=150.00)
        Trade.objects.create(portfolio=portfolio1, symbol='GOOGL', quantity=5, price=2800.00)
        Trade.objects.create(portfolio=portfolio2, symbol='TSLA', quantity=2, price=700.00)

        self.stdout.write(self.style.SUCCESS('Successfully seeded initial data'))