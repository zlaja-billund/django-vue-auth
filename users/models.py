from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class PasswordReset(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
    )

    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

