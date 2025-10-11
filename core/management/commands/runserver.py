import threading
import time
from django.core.management.commands.runserver import Command as BaseRunserverCommand
from django.core.management import call_command
from django.utils import timezone


class Command(BaseRunserverCommand):
    def handle(self, *args, **options):
        # Start the periodic earnings task in a separate thread
        def run_daily_earnings():
            while True:
                # Run the command
                try:
                    call_command('add_daily_earnings')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error running add_daily_earnings: {e}'))

                # Sleep for 24 hours (86400 seconds)
                time.sleep(86400)

        # Start the thread
        earnings_thread = threading.Thread(target=run_daily_earnings, daemon=True)
        earnings_thread.start()

        # Run the original runserver
        super().handle(*args, **options)