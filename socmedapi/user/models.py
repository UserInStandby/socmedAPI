from django.db import models

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for the User model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user."""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Crete and save a new superuser."""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model."""
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
