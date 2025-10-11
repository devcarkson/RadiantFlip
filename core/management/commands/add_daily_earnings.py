from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import FinancialStatistic, InvestmentPlan, UserProfile, UserBalance
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Add daily earnings to users with active deposits'

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Get all users with active_deposit > 0
        active_users = FinancialStatistic.objects.filter(
            statistic_type='active_deposit',
            amount__gt=Decimal('0')
        ).values_list('user', flat=True).distinct()

        for user_id in active_users:
            try:
                user = User.objects.get(id=user_id)
                # Get or create UserProfile
                profile, created = UserProfile.objects.get_or_create(user=user)

                # Check if earnings were already added today
                if profile.last_earnings_date == today:
                    self.stdout.write(
                        self.style.WARNING(f'Earnings already added today for {user.username}')
                    )
                    continue

                # Get active_deposit amount
                active_deposit_stat = FinancialStatistic.objects.get(
                    user=user, statistic_type='active_deposit'
                )
                amount = active_deposit_stat.amount

                # Get active_plan
                active_plan_stat = FinancialStatistic.objects.get(
                    user=user, statistic_type='active_plan'
                )
                plan_id = int(active_plan_stat.amount)

                # Map to plan name
                plan_names = {1: 'LITE', 2: 'STANDARD', 3: 'PREMIUM', 4: 'DIAMOND'}
                plan_name = plan_names.get(plan_id)
                if not plan_name:
                    self.stdout.write(
                        self.style.WARNING(f'Invalid plan_id {plan_id} for user {user.username}')
                    )
                    continue

                # Get percentage
                try:
                    plan = InvestmentPlan.objects.get(name=plan_name)
                    percentage = plan.daily_percentage
                except InvestmentPlan.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'InvestmentPlan {plan_name} not found')
                    )
                    continue

                # Calculate daily earnings
                daily_earn = amount * (Decimal(percentage) / 100)

                # Add to total_earned
                total_earned_stat, created = FinancialStatistic.objects.get_or_create(
                    user=user, statistic_type='total_earned', defaults={'amount': Decimal('0.00')}
                )
                total_earned_stat.amount += daily_earn
                total_earned_stat.save()

                # Add to user's balance
                user_balance, created = UserBalance.objects.get_or_create(
                    user=user, defaults={'balance': Decimal('0.00')}
                )
                user_balance.balance += daily_earn
                user_balance.save()

                # Update last_earnings_date
                profile.last_earnings_date = today
                profile.save()

                self.stdout.write(
                    self.style.SUCCESS(f'Added ${daily_earn} to {user.username}\'s total_earned and balance')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing user {user_id}: {e}')
                )

        self.stdout.write(self.style.SUCCESS('Daily earnings added successfully'))