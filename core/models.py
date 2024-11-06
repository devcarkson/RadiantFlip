from time import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)  # Ensure this field exists
    country = models.CharField(max_length=100)
    agree = models.BooleanField(default=False)

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
        (1, 'LITE 50%'),
        (2, 'STANDARD 100%'),
        (3, 'PREMIUM 150%'),
        (4, 'DIAMOND 200%'),
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





