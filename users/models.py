from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin) :
    USER_STATUS_CHOICES = (
        (1, 'admin'),
        (2, 'user'),
    )

    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, unique=True, null=False)
    user_email = models.EmailField(max_length=70, unique=True, null=False)
    user_status = models.PositiveSmallIntegerField(choices=USER_STATUS_CHOICES, default=2, null=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_email']
    objects = CustomUserManager()