from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Contact
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserProfileRegistrationForm(UserCreationForm):
    fullname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    country = forms.CharField(max_length=100)
    agree = forms.BooleanField(required=True)

    class Meta:
        model = User  # Change to User model here
        fields = ['username', 'email', 'password1', 'password2']  # Fields that belong to User

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A user with that phone number already exists.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


from django import forms
from .models import Deposit

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount', 'payment_system', 'staking_plan']



from django import forms
from django.contrib.auth.models import User
from .models import UserProfile  # Import the UserProfile model

class UserUpdateForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'uk-input uk-text-emphasis form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'uk-input uk-text-emphasis form-control'})
    )
    country = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'uk-input uk-text-emphasis form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'uk-input uk-text-emphasis form-control'})
    )

    class Meta:
        model = User
        fields = ['email']  # Only include User fields

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Prepopulate UserProfile fields
        if user and hasattr(user, 'userprofile'):
            profile = user.userprofile
            self.fields['fullname'].initial = profile.fullname
            self.fields['phone'].initial = profile.phone
            self.fields['country'].initial = profile.country


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Save the related UserProfile
        profile = user.userprofile
        profile.fullname = self.cleaned_data['fullname']
        profile.phone = self.cleaned_data['phone']
        profile.country = self.cleaned_data['country']
        profile.save()

        return user


from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fullname', 'phone', 'country']


from django import forms
from .models import Withdraw

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['amount', 'wallet_address']  # Fields that the user will fill
