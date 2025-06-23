# backend/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom User model where email is the unique identifier for authentication.
    """
    email = models.EmailField(_('email address'), unique=True)

    # The field used for login
    USERNAME_FIELD = 'email'
    
    # Fields required when creating a user via createsuperuser
    # 'username' is still part of the model from AbstractUser, so we keep it here.
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email