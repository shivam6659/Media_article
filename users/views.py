# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import random
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import Article
from django.core.paginator import Paginator




# users/views.py
# def login_view(request):
#     # your login logic here
#     return render(request, 'login.html')


# Login View with AuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user's group membership
            if user.is_superuser:
                return redirect('admin_dashboard')  # Admin Dashboard
            elif user.groups.filter(name='Editor').exists():
                return redirect('editor_dashboard')  # Editor Dashboard
            elif user.groups.filter(name='Journalist').exists():
                return redirect('journalist_dashboard')  # Journalist Dashboard
            else:
                return redirect('home_dashboard')  # Default User Dashboard
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
         form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# Alternative Login View with Manual Authentication
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user's group membership
            if user.is_superuser:
                return redirect('default_dashboard')  # Admin Dashboard
            elif user.groups.filter(name='Editor').exists():
                return redirect('editor_dashboard')  # Editor Dashboard
            elif user.groups.filter(name='Journalist').exists():
                return redirect('journalist_dashboard')  # Journalist Dashboard
            else:
                return redirect('default_dashboard')  # Default User Dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # You can access the role like this if needed, but it's already saved by form.save() automatically
            role = form.cleaned_data['role']  
            
            # Save the user with the role
            user = form.save(commit=False)
            user.role = role  # Make sure the role is saved if not automatically handled
            user.save()

            group = Group.objects.get(name=role)
            user.groups.add(group)

            # Redirect to login page after successful registration
            return redirect('login')
        else:
            # Print form errors for debugging purposes (can be removed later)
            print(form.errors)
    
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# Function to send OTP to email
def send_otp_email(user_email, otp):
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is {otp}. It will expire in 10 minutes.'
    email_from = settings.DEFAULT_FROM_EMAIL  # Ensure you have this configured in settings.py
    send_mail(subject, message, email_from, [user_email])

# Password reset form view
def pass_reset_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Check if the email exists
            User = get_user_model()
            user = User.objects.get(email=email)

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Send OTP to the user's email
            send_otp_email(email, otp)

            # Store OTP in session (you can also store it in the database for more security)
            request.session['otp'] = otp
            request.session['email'] = email

            # You could also store the expiration time for the OTP if necessary

            # Success message
            messages.success(request, 'OTP sent to your email address. Please check your inbox.')

            return redirect('enter_otp')  # Redirect to the OTP entry page (you need to create this)

        except User.DoesNotExist:
            messages.error(request, 'Email address not found. Please try again.')

    return render(request, 'pass_reset_form.html')


def enter_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        otp_stored = request.session.get('otp')

        if otp_entered == str(otp_stored):
            # OTP is valid, now allow the user to reset the password
            return redirect('pass_reset')  # Create the view for resetting the password
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'enter_otp.html')



# def verify_otp(request):
#    return render(request, 'verify_otp.html')


def pass_reset(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if the passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('pass_reset')

        # Retrieve the email from the session
        email = request.session.get('email')

        if not email:
            messages.error(request, "Session expired. Please start the process again.")
            return redirect('pass_reset_form')

        # Get the user associated with the email
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)  # Set the new password
            user.save()  # Save the user object with the new password
            print(user.password) 

            # Clear the session data after successful password reset
            request.session.pop('email', None)
            request.session.pop('otp', None)

            messages.success(request, "Password has been successfully reset! You can now log in.")
            return redirect('login')  # Redirect to the login page
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect('login')

    return render(request, 'pass_reset.html')  # Render the password reset page





def pass_change(request):
    # Your view logic here
    return render(request, 'login.html')

# views.py
@login_required
def change_password(request):
    if request.method == 'POST':
        # Use the correct User model here
        User = get_user_model()
        
        username = request.user.username
        user = User.objects.get(username=username)

        # Your password change logic
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            if user.check_password(old_password):  # Check if the old password matches
                user.set_password(new_password)  # Set the new password
                user.save()
                return redirect('login')  # Redirect to login page after password change
            else:
                # Handle invalid old password
                return render(request, 'login.html', {'error': 'Old password is incorrect'})
        else:
            # Handle password mismatch
            return render(request, 'users/change_password.html', {'error': 'New passwords do not match'})

    return render(request, 'users/change_password.html')




#Dashboard

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def editor_dashboard(request):
    return render(request, 'editor_dashboard.html')

def journalist_dashboard(request):
    return render(request, 'journalist_dashboard.html')

def default_dashboard(request):
    return render(request, 'articles/default_dashboard.html')

def article_list(request):
    return render(request, 'articles/article_list.html')




def dashboard(request):
    # Your view logic here
    return render(request, 'dashboard.html')






