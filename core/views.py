# from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import login, authenticate, logout
from .forms import *
from .models import *
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.utils import timezone
# from decimal import Decimal




import requests
from django.shortcuts import render, redirect
from .models import Deposit
from .forms import DepositForm

# # This function fetches live conversion rates from CoinGecko for multiple cryptocurrencies
# def get_live_rate(payment_system):
#     url = 'https://api.coingecko.com/api/v3/simple/price'
#     params = {
#         'ids': 'bitcoin,ethereum,tether',  # Add more as necessary
#         'vs_currencies': 'usd'
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
    
#     if payment_system == 'Bitcoin':  # Bitcoin
#         return data['bitcoin']['usd']
#     elif payment_system == 'Ethereum':  # Ethereum
#         return data['ethereum']['usd']
#     elif payment_system == 'Litecoin':  # Litecoin
#         return data['tether']['usd']
#     return 1


# def convert_to_crypto(amount_in_usd, payment_system):
#     # Get the live rate for the selected cryptocurrency
#     rate = get_live_rate(payment_system)
#     # Convert USD to cryptocurrency
#     return amount_in_usd / rate

import requests
from decimal import Decimal

# This function fetches live conversion rates from CoinGecko for multiple cryptocurrencies
def get_live_rate(payment_system):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,litecoin',  # Ensure all necessary cryptocurrencies are listed
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Ensure the rate is returned as Decimal
    if payment_system == 'Bitcoin':  # Bitcoin
        return Decimal(data['bitcoin']['usd'])
    elif payment_system == 'Ethereum':  # Ethereum
        return Decimal(data['ethereum']['usd'])
    elif payment_system == 'Litecoin':  # Litecoin
        return Decimal(data['litecoin']['usd'])  # Correct to 'litecoin'
    return Decimal(1)  # Fallback value as Decimal


def convert_to_crypto(amount_in_usd, payment_system):
    # Get the live rate for the selected cryptocurrency
    rate = get_live_rate(payment_system)
    # Ensure amount_in_usd is Decimal for division
    amount_in_usd = Decimal(amount_in_usd)  # Convert to Decimal
    # Convert USD to cryptocurrency
    return amount_in_usd / rate



def index(request):
    # Get investment plans in order for homepage display
    plan_names = ['LITE', 'STANDARD', 'PREMIUM', 'DIAMOND']
    plans = []
    for name in plan_names:
        try:
            plan = InvestmentPlan.objects.get(name=name)
            plans.append(plan)
        except InvestmentPlan.DoesNotExist:
            plans.append(None)

    # Prepare data for calculator
    import json
    daily_rates = {}
    plan_durations = {}
    for i, plan in enumerate(plans, 1):
        if plan:
            daily_rates[i] = plan.daily_percentage
            plan_durations[i] = plan.duration_hours

    context = {
        'plans': plans,
        'plans1': plans[:2],
        'plans2': plans[2:],
        'daily_rates': json.dumps(daily_rates),
        'plan_durations': json.dumps(plan_durations)
    }
    return render(request, 'index.html', context)

def faq(request):
    context ={}
    return render(request, 'index38cd.html', context)

def terms(request):
    context ={}
    return render(request, 'indexa972.html', context)

# def contact(request):
#     context ={}
#     return render(request, 'index15a0.html', context)

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings  

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save() 

            # Notify admin about new contact form submission
            admin_email_subject = 'New Contact Form Submission at Global Regional Strategy'
            admin_email_message = (
                f"A new contact form submission has been received.\n\n"
                f"Name: {contact.name}\n"
                f"Email: {contact.email}\n"
                f"Message: {contact.message}\n\n"
                f"Please review the submission details."
            )

            plain_message = admin_email_message

            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #28a745;">New Contact Form Submission</h2>
                <p>A new contact form has been submitted on Global Regional Strategy:</p>
                <table style="border-collapse: collapse; width: 100%; max-width: 400px;">
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Name:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{contact.name}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Email:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{contact.email}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Message:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{contact.message}</td></tr>
                </table>
                <p>Please respond to this inquiry as soon as possible.</p>
            </body>
            </html>
            """

            # Send notification email to all admin emails
            send_mail(
                admin_email_subject,
                plain_message,
                'Global Regional Strategy <support@globalregionalstrategy.com>',  # Use your desired sender name and email
                list(settings.ADMIN_EMAILS),
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact') 

    else:
        form = ContactForm()

    return render(request, 'index15a0.html', {'form': form})




from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from .models import UserProfile
from .forms import UserProfileRegistrationForm

def signup(request):
    if request.method == 'POST':
        user_form = UserProfileRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # Deactivate account until email confirmation
            user.save()

            # Create UserProfile and link it to the User
            UserProfile.objects.create(
                user=user,
                fullname=user_form.cleaned_data['fullname'],
                phone=user_form.cleaned_data['phone'],
                country=user_form.cleaned_data['country'],
                agree=user_form.cleaned_data['agree']
            )

            # Create UserBalance
            UserBalance.objects.create(user=user, balance=Decimal('0.00'))

            # Generate activation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Send activation email to user
            current_site = get_current_site(request)
            mail_subject = 'Activate your Global Regional Strategy account'
            
            # Render the HTML template for the email
            html_message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            
            # Create the email
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body="Please use an email client that supports HTML to view this email.",
                from_email='Global Regional Strategy <support@globalregionalstrategy.com>',
                to=[user.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            # Notify admin about new user registration
            admin_email_subject = 'New User Registration at Global Regional Strategy'
            admin_email_message = f"A new user has registered on Global Regional Strategy.\n\nUsername: {user.username}\nEmail: {user.email}\nFull Name: {user_form.cleaned_data['fullname']}\n\nPlease review the user registration details."

            plain_message = admin_email_message

            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #17a2b8;">New User Registration</h2>
                <p>A new user has registered on Global Regional Strategy:</p>
                <table style="border-collapse: collapse; width: 100%; max-width: 400px;">
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Username:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{user.username}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Email:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{user.email}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Full Name:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{user_form.cleaned_data['fullname']}</td></tr>
                </table>
                <p>Please review the user details in the admin panel.</p>
            </body>
            </html>
            """

            # Send notification email to all admin emails
            send_mail(
                admin_email_subject,
                plain_message,
                'Global Regional Strategy <support@globalregionalstrategy.com>',
                list(settings.ADMIN_EMAILS),
                html_message=html_message,
                fail_silently=False,
            )


            messages.success(request, 'You have successfully signed up. Please check your email to activate your account.')
            return redirect('login')

        else:
            # Add each field's error to Django messages
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        user_form = UserProfileRegistrationForm()

    return render(request, 'indexcca3.html', {'form': user_form})


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def activate(request, uidb64, token):
    try:
        # Decode user id from base64
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the token is valid for the user
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate the user
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return render(request, 'activation_email.html')




from django.contrib.auth import authenticate, login as auth_login 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def login_view(request): 
    if request.method == 'POST': #CARKSONTECH
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)  
                messages.success(request, f'Welcome back, {username}!')
                return redirect('account')  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'indexc30b.html', {'form': form})


def logout_view(request):
    logout(request) 
    messages.success(request, 'You have been logged out successfully.')  
    return redirect('login')




# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages

def forgottenpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Please provide your username or email.")
            return render(request, 'index8083.html')

        # Check if the user exists
        associated_users = User.objects.filter(email=email) | User.objects.filter(username=email)
        if associated_users.exists():
            for user in associated_users:
                # Send password reset email
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.html"
                c = {
                    "email": user.email,
                    "domain": request.META['HTTP_HOST'],
                    "site_name": "Global Regional Strategy",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # Ensure uid is encoded
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": 'https' if request.is_secure() else 'http',
                }
                email_message = render_to_string(email_template_name, c)

                # Send the email with HTML content
                send_mail(
                    subject,
                    message="This is a plain text fallback message.",
                    from_email='Global Regional Strategy <support@globalregionalstrategy.com>',
                    recipient_list=[user.email],
                    html_message=email_message,
                    fail_silently=False
                )
            messages.success(request, 'A password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'No account found with that email or username.')
            return render(request, 'index8083.html')

    return render(request, 'index8083.html')


def password_reset_confirm(request):
    context = {}
    return render(request, 'password_reset_confirm.html', context)



# views.py
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Custom Password Reset Request View
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = 'password_reset_email.html'  # Your custom email template
    template_name = 'password_reset_form.html'  # Custom template for requesting password reset
    subject_template_name = 'password_reset_subject.txt'  # Optional, custom subject
    success_url = reverse_lazy('password_reset_done')
    success_message = "A link to reset your password has been sent to your email."



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Your custom template for confirming reset
    success_url = reverse_lazy('login')  # Redirect to login page after success
    
    def form_valid(self, form):
        messages.success(self.request, "Password reset successfully. You can now log in with your new password.")
        return super().form_valid(form)

# Custom Password Reset Complete View
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'  # Your custom template after password reset





from django.contrib.auth.decorators import login_required
from django.db import models
from .models import FinancialStatistic

@login_required
def account(request):
    referral_link = f"https://{request.get_host()}/?ref={request.user.username}"
    # Retrieve financial statistics for the logged-in user
    total_deposit = FinancialStatistic.objects.filter(user=request.user, statistic_type='total_deposit').aggregate(total=models.Sum('amount'))['total'] or 0
    total_withdrawal = FinancialStatistic.objects.filter(user=request.user, statistic_type='total_withdrawal').aggregate(total=models.Sum('amount'))['total'] or 0
    total_earned = FinancialStatistic.objects.filter(user=request.user, statistic_type='total_earned').aggregate(total=models.Sum('amount'))['total'] or 0
    active_deposit = FinancialStatistic.objects.filter(user=request.user, statistic_type='active_deposit').aggregate(total=models.Sum('amount'))['total'] or 0
    balance = FinancialStatistic.objects.filter(user=request.user, statistic_type='active_deposit').aggregate(total=models.Sum('amount'))['total'] or 0
    
    # Calculate balance: Total Earned - Total Withdrawals + Total Deposits
    # balance = total_earned - total_withdrawal + total_deposit
    
    # Retrieve user balance
    try:
        balance = UserBalance.objects.get(user=request.user).balance  # Assuming 'balance' is the field name
    except UserBalance.DoesNotExist:
        balance = 0  # Set balance to 0 if no record exists

    context = {
        'total_deposit': total_deposit,
        'total_withdrawal': total_withdrawal,
        'total_earned': total_earned,
        'active_deposit': active_deposit,
        'balance': balance,
        'referral_link': referral_link,
    }
    
    return render(request, 'account.html', context)


#

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Deposit
from .forms import DepositForm



from django.http import JsonResponse
from .models import Wallet

@login_required
def get_wallet_address(request):
    if request.method == 'GET':
        payment_system = request.GET.get('payment_system')
        try:
            # Fetch the wallet address for the selected payment system
            wallet = Wallet.objects.get(payment_method=payment_system)
            return JsonResponse({'wallet_address': wallet.wallet_address}, status=200)
        except Wallet.DoesNotExist:
            return JsonResponse({'error': 'Wallet not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DepositForm
from .models import Deposit


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Deposit

@login_required
def deposit(request):
    # Check if the user has any pending deposits
    pending_deposit = Deposit.objects.filter(user=request.user, status='pending').exists()

    if pending_deposit:
        # Show a message on the deposit page indicating that a pending deposit exists
        messages.error(request, "You already have a pending deposit. Please complete the existing one before creating a new deposit.")
        return render(request, 'deposit.html', {'pending': True})  # Pass a context variable to disable the form

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)  # Create deposit instance without saving
            deposit.user = request.user  # Set the user
            deposit.crypto_amount = convert_to_crypto(deposit.amount, deposit.payment_system)  # Calculate crypto amount

            # Store necessary deposit data in session without saving to the database
            request.session['deposit_data'] = {
                'amount': float(deposit.amount),
                'payment_system': deposit.payment_system,
                'crypto_amount': float(deposit.crypto_amount),
                'staking_plan': deposit.staking_plan,
            }

            # Redirect to confirmation page (without deposit_id)
            return redirect('confirm_deposit')  # No deposit_id passed here
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepositForm()

    # Get investment plans in order
    plan_names = ['LITE', 'STANDARD', 'PREMIUM', 'DIAMOND']
    plans = []
    for name in plan_names:
        try:
            plan = InvestmentPlan.objects.get(name=name)
            plans.append(plan)
        except InvestmentPlan.DoesNotExist:
            plans.append(None)

    return render(request, 'deposit.html', {'form': form, 'pending': False, 'plans': plans})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Deposit, Wallet


from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.shortcuts import render, redirect
from .models import Deposit, Wallet

from django.core.mail import send_mail
from django.conf import settings

@login_required
def confirm_deposit(request):
    deposit_data = request.session.get('deposit_data', None)

    if not deposit_data:
        messages.error(request, "No deposit data found.")
        return redirect('deposit')

    # Retrieve the wallet address based on the selected payment system
    try:
        wallet = Wallet.objects.get(payment_method=deposit_data['payment_system'])
        wallet_address = wallet.wallet_address
    except Wallet.DoesNotExist:
        wallet_address = None

    if request.method == 'POST':
        # Save the deposit
        deposit = Deposit(
            user=request.user,
            amount=deposit_data['amount'],
            payment_system=deposit_data['payment_system'],
            crypto_amount=deposit_data['crypto_amount'],
            staking_plan=deposit_data['staking_plan'],
            status='pending'
        )
        deposit.save()

        # Get plan percentage for emails
        plan_names = {1: 'LITE', 2: 'STANDARD', 3: 'PREMIUM', 4: 'DIAMOND'}
        plan_name = plan_names.get(deposit.staking_plan)
        percentage = 0
        if plan_name:
            try:
                plan = InvestmentPlan.objects.get(name=plan_name)
                percentage = plan.daily_percentage
            except InvestmentPlan.DoesNotExist:
                percentage = 0
        staking_plan_with_percent = f"{deposit.get_staking_plan_display()} {percentage}%"

        # Notify the admin via email about the new deposit
        admin_emails = list(settings.ADMIN_EMAILS)
        formatted_from_email = settings.DEFAULT_FROM_EMAIL

        plain_message = f"A new deposit has been made:\n\n" \
                        f"User: {request.user.username}\n" \
                        f"Amount: {deposit.amount}\n" \
                        f"Payment System: {deposit.get_payment_system_display()}\n" \
                        f"Crypto Amount: {deposit.crypto_amount}\n" \
                        f"Staking Plan: {staking_plan_with_percent}\n"

        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #007bff;">New Deposit Notification</h2>
            <p>A new deposit has been made on Global Regional Strategy:</p>
            <table style="border-collapse: collapse; width: 100%; max-width: 400px;">
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>User:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{request.user.username}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${deposit.amount}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Payment System:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{deposit.get_payment_system_display()}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Crypto Amount:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{deposit.crypto_amount}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Staking Plan:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{staking_plan_with_percent}</td></tr>
            </table>
            <p>Please review this deposit in the admin panel.</p>
        </body>
        </html>
        """

        send_mail(
            subject=f'New Deposit by {request.user.username}',
            message=plain_message,
            from_email=formatted_from_email,
            recipient_list=admin_emails,
            html_message=html_message,
            fail_silently=False,
        )

        # Send notification email to user about pending deposit
        user_plain_message = f"Dear {request.user.username},\n\n" \
                            f"Your deposit request has been submitted successfully.\n\n" \
                            f"Details:\n" \
                            f"Amount: ${deposit.amount}\n" \
                            f"Payment System: {deposit.get_payment_system_display()}\n" \
                            f"Crypto Amount: {deposit.crypto_amount}\n" \
                            f"Staking Plan: {staking_plan_with_percent}\n\n" \
                            f"Status: Pending\n\n" \
                            f"Your deposit is currently under review. You will receive a confirmation email once it has been processed.\n\n" \
                            f"Thank you for choosing Global Regional Strategy!"

        user_html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px;">
                <h2 style="color: #007bff; text-align: center;">Deposit Request Submitted</h2>
                <p>Dear {request.user.username},</p>
                <p>Your deposit request has been submitted successfully on Global Regional Strategy.</p>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Deposit Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${deposit.amount}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Payment System:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{deposit.get_payment_system_display()}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Crypto Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{deposit.crypto_amount}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Staking Plan:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{staking_plan_with_percent}</td></tr>
                        <tr><td style="padding: 8px;"><strong>Status:</strong></td><td style="padding: 8px;"><span style="color: #ffc107; font-weight: bold;">Pending Review</span></td></tr>
                    </table>
                </div>
                <p>Your deposit is currently under review. You will receive a confirmation email once it has been processed.</p>
                <p>Thank you for choosing Global Regional Strategy!</p>
                <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                    <p>&copy; 2025 Global Regional Strategy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        send_mail(
            subject='Deposit Request Submitted - Global Regional Strategy',
            message=user_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            html_message=user_html_message,
            fail_silently=False,
        )

        # Clear session after saving deposit
        del request.session['deposit_data']

        messages.success(request, "Deposit confirmed and saved successfully!")
        return redirect('account')

    # Get dynamic plan details
    plan_names = {1: 'LITE', 2: 'STANDARD', 3: 'PREMIUM', 4: 'DIAMOND'}
    plan_name = plan_names.get(deposit_data['staking_plan'], 'Unknown')
    percentage = 0
    if plan_name != 'Unknown':
        try:
            plan = InvestmentPlan.objects.get(name=plan_name)
            percentage = plan.daily_percentage
        except InvestmentPlan.DoesNotExist:
            percentage = 0
    staking_plan_display = f"{plan_name} {percentage}%"

    return render(request, 'confirm_deposit.html', {
        'deposit_data': deposit_data,
        'staking_plan_display': staking_plan_display,
        'percentage': percentage,
        'wallet_address': wallet_address,
        'site_name': "Global Regional Strategy"
    })




import logging

logger = logging.getLogger(__name__)




from django.shortcuts import render
from django.utils import timezone
from .models import Deposit, Withdraw, Stake  # Make sure to import Stake model

def history(request):
    now = timezone.now()
    months = [
        (1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'),
        (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'),
        (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')
    ]
    days = list(range(1, 32))
    years = [2023, 2024, 2025]

    # Get filter inputs from GET request
    transaction_type = request.GET.get('type', 'all')
    ecurrency = request.GET.get('ec', 'all')
    month_from = request.GET.get('month_from', now.month)
    day_from = request.GET.get('day_from', now.day)
    year_from = request.GET.get('year_from', now.year)
    month_to = request.GET.get('month_to', now.month)
    day_to = request.GET.get('day_to', now.day)
    year_to = request.GET.get('year_to', now.year)

    from_date = timezone.datetime(year=int(year_from), month=int(month_from), day=int(day_from))
    to_date = timezone.datetime(year=int(year_to), month=int(month_to), day=int(day_to), hour=23, minute=59, second=59)

    # Filter deposits and withdrawals based on the date range
    deposits = Deposit.objects.filter(
        created_at__range=(from_date, to_date),
        user=request.user
    )
    withdrawals = Withdraw.objects.filter(
        date_created__range=(from_date, to_date),
        user=request.user
    )
    
    # Filter stakes based on the date range
    stakes = Stake.objects.filter(
        date_staked__range=(from_date, to_date),  # Use the correct field for Stake model
        user=request.user
    )

    # Combine all transactions
    transactions = []

    for deposit in deposits:
        transactions.append({
            'type': 'Deposit',
            'amount': deposit.amount,
            'date': deposit.created_at,
            'payment_system': deposit.payment_system
        })

    for withdrawal in withdrawals:
        transactions.append({
            'type': 'Withdrawal',
            'amount': withdrawal.amount,
            'date': withdrawal.date_created,
            'payment_system': None
        })

    for stake in stakes:
        transactions.append({
            'type': 'Stake',
            'amount': stake.amount,
            'date': stake.date_staked,  
            'payment_system': None
        })

    # Apply filters based on transaction type
    if transaction_type != 'all':
        transactions = [txn for txn in transactions if txn['type'] == transaction_type]

    # Apply filters based on eCurrency (only applicable for deposits)
    if ecurrency != 'all':
        transactions = [txn for txn in transactions if txn['payment_system'] == ecurrency]

    # Sort transactions by date
    transactions.sort(key=lambda txn: txn['date'])

    context = {
        'transactions': transactions,
        'transaction_type': transaction_type,
        'ecurrency': ecurrency,
        'from_date': from_date,
        'to_date': to_date,
        'now': now,
        'months': months,
        'days': days,
        'years': years,
    }
    return render(request, 'history.html', context)





@login_required
def referral(request):
    # Generate the referral link dynamically based on the current site URL
    referral_link = f"https://{request.get_host()}/?ref={request.user.username}"
    
    # Get referral statistics (you will need to implement these queries)
    total_referrals = Referral.objects.filter(referrer=request.user).count()
    active_referrals = Referral.objects.filter(referrer=request.user, status='active').count()
    total_earnings = sum(referral.earnings for referral in Referral.objects.filter(referrer=request.user))

    context = {
        'referral_link': referral_link,
        'total_referrals': total_referrals,
        'active_referrals': active_referrals,
        'total_earnings': total_earnings,
    }
    
    return render(request, 'referral.html', context)



from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserUpdateForm

@login_required
def edit_account(request):
    user = request.user
    try:
        # Try to get the user's profile
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # If the profile does not exist, create one
        user_profile = UserProfile(user=user)
        user_profile.save()

    if request.method == 'POST':
        # Use the form to update both user and user profile information
        user_form = UserUpdateForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()  # Save user details
            messages.success(request, 'Your account has been successfully updated.')
            return redirect('edit_account')
        else:
            # Handle form validation errors
            messages.error(request, 'There was an error updating your account. Please check the form.')

    else:
        # Initialize the form with the user's current data
        user_form = UserUpdateForm(instance=user)

    return render(request, 'edit_account.html', {
        'user_form': user_form,
        'user_profile': user_profile
    })



import pyotp
import qrcode
from io import BytesIO
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import urllib.parse
import base64

def security(request):
    if request.method == 'POST':
        # Handle form submissions
        ip_sensitivity = request.POST.get('ip', 'disabled')
        browser_change = request.POST.get('browser', 'disabled')

        return redirect(reverse('security'))

    # Generate a new TOTP secret
    totp = pyotp.TOTP(pyotp.random_base32())
    secret_key = totp.secret

    # Create the TOTP URI
    current_site = request.get_host()  # Get the current domain
    totp_uri = f"otpauth://totp/{urllib.parse.quote(current_site)}?secret={secret_key}"

    # Generate the QR code with a custom size
    qr = qrcode.QRCode(
        version=1,  # controls the size of the code (1 is a small version)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,  # size of each "box" in the QR code
        border=1,    # border size around the QR code
    )
    qr.add_data(totp_uri)
    qr.make(fit=True)

    # Create the image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    context = {
        'tfa_secret': secret_key,
        'qr_code_base64': qr_code_base64,  # Use base64 image
    }

    return render(request, 'security.html', context)



from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import UserBalance, Withdraw
from .forms import WithdrawalForm

@login_required
def withdrawal(request):
    # Attempt to retrieve the user's balance
    try:
        user_balance = UserBalance.objects.get(user=request.user)
        balance = user_balance.balance
    except UserBalance.DoesNotExist:
        balance = Decimal('0.00')  # Set balance to 0 if no record exists

    # Check for pending withdrawals and calculate total pending amount
    pending_withdrawals_query = Withdraw.objects.filter(user=request.user, status='pending')
    pending_withdrawals_total = pending_withdrawals_query.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    if pending_withdrawals_query.exists():
        messages.error(request, "You already have a pending withdrawal. Please complete the existing one before creating a new withdrawal.")
        return render(request, 'withdraw.html', {'balance': balance, 'pending_withdrawals': pending_withdrawals_total, 'pending': True})

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)  
            withdrawal.user = request.user  # Set the user

            # Check if the user has enough balance
            if withdrawal.amount > balance:
                messages.error(request, "Insufficient balance to make this withdrawal.")
                return render(request, 'withdraw.html', {'form': form, 'balance': balance, 'pending_withdrawals': pending_withdrawals_total, 'pending': False})

            # Deduct the withdrawal amount from the balance
            user_balance.balance -= withdrawal.amount
            user_balance.save()

            # Save withdrawal request to the database
            withdrawal.status = 'pending'  # Add 'pending' status for review
            withdrawal.save()

            # Notify the admin via email about the new withdrawal
            admin_emails = list(settings.ADMIN_EMAILS)
            formatted_from_email = settings.DEFAULT_FROM_EMAIL

            plain_message = f"A new withdrawal has been requested:\n\n" \
                            f"User: {request.user.username}\n" \
                            f"Amount: ${withdrawal.amount}\n" \
                            f"Wallet Address: {withdrawal.wallet_address}\n"

            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #dc3545;">New Withdrawal Request</h2>
                <p>A new withdrawal request has been submitted on Global Regional Strategy:</p>
                <table style="border-collapse: collapse; width: 100%; max-width: 400px;">
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>User:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{request.user.username}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${withdrawal.amount}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Wallet Address:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{withdrawal.wallet_address}</td></tr>
                </table>
                <p>Please review and approve/reject this withdrawal in the admin panel.</p>
            </body>
            </html>
            """

            send_mail(
                subject=f'New Withdrawal Request from {request.user.username}',
                message=plain_message,
                from_email=formatted_from_email,
                recipient_list=admin_emails,
                html_message=html_message,
                fail_silently=False,
            )

            # Send notification email to user about pending withdrawal
            user_plain_message = f"Dear {request.user.username},\n\n" \
                                f"Your withdrawal request has been submitted successfully.\n\n" \
                                f"Details:\n" \
                                f"Amount: ${withdrawal.amount}\n" \
                                f"Wallet Address: {withdrawal.wallet_address}\n\n" \
                                f"Status: Pending Review\n\n" \
                                f"Your withdrawal request is currently under review. You will receive a confirmation email once it has been processed.\n\n" \
                                f"Thank you for choosing Global Regional Strategy!"

            user_html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px;">
                    <h2 style="color: #dc3545; text-align: center;">Withdrawal Request Submitted</h2>
                    <p>Dear {request.user.username},</p>
                    <p>Your withdrawal request has been submitted successfully on Global Regional Strategy.</p>
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3>Withdrawal Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${withdrawal.amount}</td></tr>
                            <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Wallet Address:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{withdrawal.wallet_address}</td></tr>
                            <tr><td style="padding: 8px;"><strong>Status:</strong></td><td style="padding: 8px;"><span style="color: #ffc107; font-weight: bold;">Pending Review</span></td></tr>
                        </table>
                    </div>
                    <p>Your withdrawal request is currently under review. You will receive a confirmation email once it has been processed.</p>
                    <p>Thank you for choosing Global Regional Strategy!</p>
                    <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                        <p>&copy; 2025 Global Regional Strategy. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_mail(
                subject='Withdrawal Request Submitted - Global Regional Strategy',
                message=user_plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                html_message=user_html_message,
                fail_silently=False,
            )

            # Store necessary withdrawal data in session
            request.session['withdrawal_data'] = {
                'amount': float(withdrawal.amount),
                'wallet_address': withdrawal.wallet_address,
            }

            # Redirect to confirmation page
            messages.success(request, "Withdrawal placed successfully!")
            return redirect('account')
            
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WithdrawalForm()

    # Pass balance and pending withdrawals to the template
    return render(request, 'withdraw.html', {
        'form': form,
        'balance': balance,
        'pending_withdrawals': pending_withdrawals_total,
        'pending': False
    })




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InvestmentPlan, Stake, UserBalance

@login_required
def stake(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')  # Corrected typo here
        amount = request.POST.get('amount')

        # Get the selected plan
        try:
            plan = InvestmentPlan.objects.get(name=plan_id)
        except InvestmentPlan.DoesNotExist:
            messages.error(request, "Selected investment plan does not exist.")
            return redirect('stake')

        # Validate the amount
        try:
            amount = int(amount)  # Use float for DecimalField compatibility
        except ValueError:
            messages.error(request, "Invalid amount.")
            return redirect('stake')

        if amount < plan.min_amount or (plan.max_amount and amount > plan.max_amount):
            messages.error(request, f"Amount must be between ${plan.min_amount} and ${plan.max_amount or 'Unlimited'}.")
            return redirect('stake')

        # Get the user's balance
        try:
            user_balance = UserBalance.objects.get(user=request.user)
        except UserBalance.DoesNotExist:
            messages.error(request, "User balance not found.")
            return redirect('stake')

        # Check if the user has enough balance
        if user_balance.balance < amount:
            messages.error(request, "Insufficient balance.")
            return redirect('stake')

        # Deduct the amount from the user's balance
        user_balance.balance -= amount
        user_balance.save()

        # Create the stake
        stake = Stake.objects.create(user=request.user, plan=plan, amount=amount)

        # Send confirmation email to user
        user_plain_message = f"Dear {request.user.username},\n\n" \
                            f"Congratulations! Your staking has been processed successfully.\n\n" \
                            f"Staking Details:\n" \
                            f"Amount: ${stake.amount}\n" \
                            f"Plan: {plan.get_name_display()} ({plan.daily_percentage}% daily)\n" \
                            f"Date Staked: {stake.date_staked.strftime('%Y-%m-%d %H:%M:%S')}\n\n" \
                            f"You will start earning daily returns based on your selected plan.\n\n" \
                            f"Thank you for choosing Global Regional Strategy!"

        user_html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px;">
                <h2 style="color: #28a745; text-align: center;">Staking Confirmed!</h2>
                <p>Dear {request.user.username},</p>
                <p>Congratulations! Your staking has been processed successfully on Global Regional Strategy.</p>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Staking Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">${stake.amount}</td></tr>
                        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Plan:</strong></td><td style="padding: 8px; border-bottom: 1px solid #ddd;">{plan.get_name_display()} ({plan.daily_percentage}% daily)</td></tr>
                        <tr><td style="padding: 8px;"><strong>Date Staked:</strong></td><td style="padding: 8px;">{stake.date_staked.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                    </table>
                </div>
                <p>You will start earning daily returns based on your selected plan.</p>
                <p>Thank you for choosing Global Regional Strategy!</p>
                <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                    <p>&copy; 2025 Global Regional Strategy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        send_mail(
            subject='Staking Confirmed - Global Regional Strategy',
            message=user_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            html_message=user_html_message,
            fail_silently=False,
        )

        # Notify admin about new stake
        admin_plain_message = f"A new staking has been made:\n\n" \
                             f"User: {request.user.username}\n" \
                             f"Amount: ${stake.amount}\n" \
                             f"Plan: {plan.get_name_display()} ({plan.daily_percentage}% daily)\n" \
                             f"Date Staked: {stake.date_staked.strftime('%Y-%m-%d %H:%M:%S')}\n"

        admin_html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #17a2b8;">New Staking Notification</h2>
            <p>A new staking has been made on Global Regional Strategy:</p>
            <table style="border-collapse: collapse; width: 100%; max-width: 400px;">
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>User:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{request.user.username}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Amount:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${stake.amount}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Plan:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{plan.get_name_display()} ({plan.daily_percentage}% daily)</td></tr>
                <tr><td style="padding: 8px;"><strong>Date Staked:</strong></td><td style="padding: 8px;">{stake.date_staked.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
            </table>
            <p>Please review the staking details.</p>
        </body>
        </html>
        """

        send_mail(
            subject=f'New Staking by {request.user.username}',
            message=admin_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(settings.ADMIN_EMAILS),
            html_message=admin_html_message,
            fail_silently=False,
        )

        messages.success(request, f"You have successfully staked ${amount} in the {plan.get_name_display()}.")
        return redirect('account')  # Ensure 'account' is the correct URL for the next page

    # Render the page if the request is GET
    plan_names = ['LITE', 'STANDARD', 'PREMIUM', 'DIAMOND']
    plans = []
    for name in plan_names:
        try:
            plan = InvestmentPlan.objects.get(name=name)
            plans.append(plan)
        except InvestmentPlan.DoesNotExist:
            plans.append(None)

    # Prepare data for calculator
    import json
    daily_rates = {}
    plan_durations = {}
    for i, plan in enumerate(plans, 1):
        if plan:
            daily_rates[i] = plan.daily_percentage
            plan_durations[i] = plan.duration_hours

    context = {
        'plans': plans,
        'daily_rates': json.dumps(daily_rates),
        'plan_durations': json.dumps(plan_durations)
    }
    return render(request, 'invest.html', context)
