from django.core.management.commands.runserver import Command as BaseRunserverCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command
from django.conf import settings
import os


class Command(BaseRunserverCommand):
    def handle(self, *args, **options):
        # Initialize the scheduler
        scheduler = BackgroundScheduler()

        # Add the daily earnings job to run at midnight UTC every day
        scheduler.add_job(
            self.run_daily_earnings,
            trigger=CronTrigger(hour=0, minute=0),  # Run at 00:00 UTC every day
            id='daily_earnings',
            name='Add Daily Earnings',
            replace_existing=True,
        )

        # Start the scheduler
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Daily earnings scheduler started'))

        try:
            # Run the original runserver
            super().handle(*args, **options)
        except KeyboardInterrupt:
            # Shutdown the scheduler on exit
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('Daily earnings scheduler stopped'))

    def run_daily_earnings(self):
        """Run the add_daily_earnings management command"""
        try:
            call_command('add_daily_earnings')
            self.stdout.write(self.style.SUCCESS('Daily earnings added successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running add_daily_earnings: {e}'))