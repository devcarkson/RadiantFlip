from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)  # Ensure this field exists
    country = models.CharField(max_length=100)
    agree = models.BooleanField(default=False)
    last_earnings_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.fullname




class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    



class Wallet(models.Model):
    PAYMENT_CHOICES = [
        ('Bitcoin', 'Bitcoin'),
        ('Litecoin', 'Litecoin'),
        ('Ethereum', 'Ethereum'),
        # Add more payment methods as needed
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, unique=True)
    wallet_address = models.CharField(max_length=255)  # Store the wallet address
    created_at = models.DateTimeField(auto_now_add=True)  # Store the creation timestamp

    def __str__(self):
        return f"{self.payment_method}"


from django.utils import timezone

class Deposit(models.Model):
    PAYMENT_CHOICES = [
        ('Bitcoin', 'Bitcoin'),
        ('Litecoin', 'Litecoin'),
        ('Ethereum', 'Ethereum'),
    ]

    PLAN_CHOICES = [
        (1, 'LITE'),
        (2, 'STANDARD'),
        (3, 'PREMIUM'),
        (4, 'DIAMOND'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store amount in USD
    payment_system = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    crypto_amount = models.DecimalField(max_digits=10, decimal_places=4)
    staking_plan = models.IntegerField(choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.get_payment_system_display()} - {self.amount} USD - {self.status}"



from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

class Withdraw(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    wallet_address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Withdrawal of ${self.amount} by {self.user.username}"


class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referred_user.username}"



from django.contrib.auth.models import User
from django.db import models

class FinancialStatistic(models.Model):
    STATISTIC_TYPE_CHOICES = [
        ('total_deposit', 'Total Deposit'),
        ('total_withdrawal', 'Total Withdrawal'),
        ('total_earned', 'Total Earned'),
        ('active_deposit', 'Active Deposit'),
        ('active_plan', 'Active Plan'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="statistics")
    statistic_type = models.CharField(max_length=30, choices=STATISTIC_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_statistic_type_display()}"
    
    def get_statistic_type_display(self):
        return dict(self.STATISTIC_TYPE_CHOICES).get(self.statistic_type, self.statistic_type)

    class Meta:
        verbose_name = "Financial Statistic"
        verbose_name_plural = "Financial Statistics"


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="balance")
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Balance"




from django.db import models
from django.contrib.auth.models import User

class InvestmentPlan(models.Model):
    PLAN_CHOICES = [
        ('LITE', 'Lite Plan'),
        ('STANDARD', 'Standard Plan'),
        ('PREMIUM', 'Premium Plan'),
        ('DIAMOND', 'Diamond Plan'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    daily_percentage = models.IntegerField()
    duration_hours = models.PositiveIntegerField()  # e.g., 48 hours
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., $300
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # e.g., Unlimited
    principal_return = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()
class Stake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_staked = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - ${self.amount}"


@receiver(post_save, sender=Deposit)
def handle_deposit_status_change(sender, instance, created, **kwargs):
    if not created and instance.status == 'confirmed':
        # Map staking_plan to plan name
        plan_names = {
            1: 'LITE',
            2: 'STANDARD',
            3: 'PREMIUM',
            4: 'DIAMOND',
        }
        plan_name = plan_names.get(instance.staking_plan)
        percentage = 0
        if plan_name:
            try:
                plan = InvestmentPlan.objects.get(name=plan_name)
                percentage = plan.daily_percentage
            except InvestmentPlan.DoesNotExist:
                percentage = 0

        # Update total_deposit: increment by deposit amount
        total_deposit_stat, created = FinancialStatistic.objects.get_or_create(
            user=instance.user, statistic_type='total_deposit', defaults={'amount': Decimal('0.00')}
        )
        total_deposit_stat.amount += instance.amount
        total_deposit_stat.save()

        # Update active_deposit: set to deposit amount (replace previous)
        active_deposit_stat, created = FinancialStatistic.objects.get_or_create(
            user=instance.user, statistic_type='active_deposit', defaults={'amount': Decimal('0.00')}
        )
        active_deposit_stat.amount = instance.amount
        active_deposit_stat.save()

        # Update active_plan: set to staking_plan
        active_plan_stat, created = FinancialStatistic.objects.get_or_create(
            user=instance.user, statistic_type='active_plan', defaults={'amount': Decimal('0')}
        )
        active_plan_stat.amount = instance.staking_plan
        active_plan_stat.save()

        # Note: Daily earnings will be added by a periodic task (every 24 hours)

        # Credit the user's balance
        user_balance, created = UserBalance.objects.get_or_create(user=instance.user, defaults={'balance': Decimal('0.00')})
        user_balance.balance += instance.amount
        user_balance.save()

        # Get staking plan with percentage for emails
        plan_names = {1: 'LITE', 2: 'STANDARD', 3: 'PREMIUM', 4: 'DIAMOND'}
        plan_name = plan_names.get(instance.staking_plan)
        staking_plan_with_percent = f"{instance.get_staking_plan_display()} {percentage}%"

        # Send confirmation email to user
        user_plain_message = f"Dear {instance.user.username},\n\n" \
                            f"Congratulations! Your deposit has been confirmed and processed.\n\n" \
                            f"Deposit Details:\n" \
                            f"Amount: ${instance.amount}\n" \
                            f"Payment System: {instance.get_payment_system_display()}\n" \
                            f"Crypto Amount: {instance.crypto_amount}\n" \
                            f"Staking Plan: {staking_plan_with_percent}\n\n" \
                            f"The funds have been credited to your account balance.\n\n" \
                            f"Thank you for choosing Global Regional Strategy!"

        user_html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px;">
                <h2 style="color: #28a745; text-align: center;">Deposit Confirmed!</h2>
                <p>Dear {instance.user.username},</p>
                <p>Congratulations! Your deposit has been confirmed and processed on Global Regional Strategy.</p>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Deposit Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${instance.amount}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Payment System:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{instance.get_payment_system_display()}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Crypto Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{instance.crypto_amount}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Staking Plan:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{staking_plan_with_percent}</td></tr>
                        <tr><td style="padding: 8px;"><strong>Status:</strong></td><td style="padding: 8px;"><span style="color: #28a745; font-weight: bold;">Confirmed</span></td></tr>
                    </table>
                </div>
                <p>The funds have been credited to your account balance. You can now use them for staking or withdrawals.</p>
                <p>Thank you for choosing Global Regional Strategy!</p>
                <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                    <p>&copy; 2025 Global Regional Strategy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        send_mail(
            subject='Deposit Confirmed - Global Regional Strategy',
            message=user_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            html_message=user_html_message,
            fail_silently=False,
        )


@receiver(post_save, sender=Withdraw)
def handle_withdrawal_status_change(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'approved':
            # Send approval email
            user_plain_message = f"Dear {instance.user.username},\n\n" \
                                f"Your withdrawal request has been approved and processed.\n\n" \
                                f"Withdrawal Details:\n" \
                                f"Amount: ${instance.amount}\n" \
                                f"Wallet Address: {instance.wallet_address}\n\n" \
                                f"The funds have been sent to your wallet.\n\n" \
                                f"Thank you for choosing Global Regional Strategy!"

            user_html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px;">
                    <h2 style="color: #28a745; text-align: center;">Withdrawal Approved!</h2>
                    <p>Dear {instance.user.username},</p>
                    <p>Your withdrawal request has been approved and processed on Global Regional Strategy.</p>
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3>Withdrawal Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${instance.amount}</td></tr>
                            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Wallet Address:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{instance.wallet_address}</td></tr>
                            <tr><td style="padding: 8px;"><strong>Status:</strong></td><td style="padding: 8px;"><span style="color: #28a745; font-weight: bold;">Approved</span></td></tr>
                        </table>
                    </div>
                    <p>The funds have been sent to your wallet. Please check your wallet for confirmation.</p>
                    <p>Thank you for choosing Global Regional Strategy!</p>
                    <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                        <p>&copy; 2025 Global Regional Strategy. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

        elif instance.status == 'rejected':
            # Refund the balance
            user_balance, created = UserBalance.objects.get_or_create(user=instance.user, defaults={'balance': Decimal('0.00')})
            user_balance.balance += instance.amount
            user_balance.save()

            # Send rejection email
            user_plain_message = f"Dear {instance.user.username},\n\n" \
                                f"Your withdrawal request has been rejected.\n\n" \
                                f"Withdrawal Details:\n" \
                                f"Amount: ${instance.amount}\n" \
                                f"Wallet Address: {instance.wallet_address}\n\n" \
                                f"The funds have been refunded to your account balance.\n\n" \
                                f"If you have any questions, please contact our support team.\n\n" \
                                f"Thank you for choosing Global Regional Strategy!"

            user_html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px;">
                    <h2 style="color: #dc3545; text-align: center;">Withdrawal Rejected</h2>
                    <p>Dear {instance.user.username},</p>
                    <p>Your withdrawal request has been rejected on Global Regional Strategy.</p>
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3>Withdrawal Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${instance.amount}</td></tr>
                            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Wallet Address:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{instance.wallet_address}</td></tr>
                            <tr><td style="padding: 8px;"><strong>Status:</strong></td><td style="padding: 8px;"><span style="color: #dc3545; font-weight: bold;">Rejected</span></td></tr>
                        </table>
                    </div>
                    <p>The funds have been refunded to your account balance. If you have any questions about this decision, please contact our support team.</p>
                    <p>Thank you for choosing Global Regional Strategy!</p>
                    <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                        <p>&copy; 2025 Global Regional Strategy. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

        send_mail(
            subject=f'Withdrawal {instance.status.title()} - Global Regional Strategy',
            message=user_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            html_message=user_html_message,
            fail_silently=False,
        )





