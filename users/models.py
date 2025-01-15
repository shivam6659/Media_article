# from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# from django.contrib.auth.models import User


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Journalist', 'Journalist'),
        ('Editor', 'Editor'),
        ('Admin', 'Admin'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
    


class OTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use the dynamic user model reference
        on_delete=models.CASCADE
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Check if the OTP is still valid (e.g., within 10 minutes)."""
        from datetime import timedelta, timezone
        return self.created_at >= timezone.now() - timedelta(minutes=10)
    
    # users/models.py


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
    # Add any other custom fields if needed

# users/models.py
# from django.conf import settings

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)












