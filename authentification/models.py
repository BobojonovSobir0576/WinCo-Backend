from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group


class CustomUser(AbstractUser):
    is_varified = models.BooleanField(default=False)

