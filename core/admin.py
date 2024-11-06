from . models import *

# admin.site.register(UserProfile)

# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(InvestmentPlan)
admin.site.register(Wallet)
admin.site.register(Contact)
# admin.site.register(Investment)

# from django.contrib import admin
# from .models import Deposit

# @admin.register(Deposit)
# class DepositAdmin(admin.ModelAdmin):
#     list_display = ('user', 'payment_system', 'amount', 'crypto_amount', 'created_at')
#     search_fields = ('user__username', 'payment_system',)

# from django.contrib import admin
# from .models import Withdraw

# @admin.register(Withdraw)
# class WithdrawAdmin(admin.ModelAdmin):
#     list_display = ('user', 'amount', 'wallet_address', 'date_created')
#     list_filter = ('date_created',)
#     search_fields = ('user__username', 'wallet_address')

from django.contrib import admin
from .models import Deposit, Withdraw

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_system', 'amount', 'crypto_amount', 'created_at')
    search_fields = ('user__username', 'payment_system',)
    fields = ('user', 'payment_system', 'amount', 'crypto_amount', 'staking_plan', 'status', 'created_at')  # Include created_at for editing

@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'wallet_address', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('user__username', 'wallet_address')
    fields = ('user', 'amount', 'wallet_address', 'status', 'date_created')  # Include date_created for editing



from django.contrib import admin
from .models import FinancialStatistic, UserBalance

@admin.register(FinancialStatistic)
class FinancialStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'statistic_type', 'amount', 'created_at')
    list_filter = ('statistic_type',)
    search_fields = ('user__username',)

@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)




from django.contrib import admin
from .models import Stake

class StakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'amount', 'date_staked', 'active']
    list_filter = ['plan', 'active']
    search_fields = ['user__username', 'plan__name']
    # Allow the 'date_staked' field to be editable
    fields = ['user', 'plan', 'amount', 'date_staked', 'active']

    # Optionally, you can override the save_model method to set the date if it's not provided
    def save_model(self, request, obj, form, change):
        if not obj.date_staked:
            from django.utils import timezone
            obj.date_staked = timezone.now()
        super().save_model(request, obj, form, change)

admin.site.register(Stake, StakeAdmin)



