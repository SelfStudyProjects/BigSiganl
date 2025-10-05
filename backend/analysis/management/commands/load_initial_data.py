from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Load initial data from JSON files'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        trades_file = os.path.join(base_dir, 'trades_data.json')
        portfolios_file = os.path.join(base_dir, 'portfolios_data.json')
        
        if os.path.exists(trades_file):
            self.stdout.write('Loading trades data...')
            call_command('loaddata', trades_file)
            self.stdout.write(self.style.SUCCESS('✓ Trades data loaded'))
        
        if os.path.exists(portfolios_file):
            self.stdout.write('Loading portfolios data...')
            call_command('loaddata', portfolios_file)
            self.stdout.write(self.style.SUCCESS('✓ Portfolios data loaded'))
        
        self.stdout.write(self.style.SUCCESS('All data loaded successfully!'))