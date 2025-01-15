from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model  # Use this to get the custom user model
from .models import User  # Assuming this is your custom User model
from django.contrib.auth.forms import AuthenticationForm

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()  # Use get_user_model() to ensure compatibility with custom User model
        fields = ['username', 'email', 'password1', 'password2', 'role']

# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom form to handle password reset using the custom User model.
    """
    def get_users(self, email):
        """
        Override this method to search users in your custom User model.
        """
        # Use get_user_model() to ensure compatibility with custom user model
        active_users = get_user_model().objects.filter(email=email, is_active=True)
        return active_users
    







    # forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']













