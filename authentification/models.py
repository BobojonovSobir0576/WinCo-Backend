from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group


class Gender(models.Model):
    g_name = models.CharField(max_length=10, blank=True, null=True, verbose_name='Gender name')

    def __str__(self):
        return self.g_name

    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Gender"

class CustomUser(AbstractUser):
    age = models.IntegerField(default=7, blank=True, null=True, verbose_name='Age')
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='Email')
    gender_id = models.ForeignKey(Gender, on_delete=models.CASCADE,null=True, blank=True, verbose_name='Gender', related_name='gender')
    about_me = models.TextField(null=True, blank=True, verbose_name='About me')
    interests = models.CharField(max_length=255, null=True, blank=True, verbose_name='About Interests')
    location_lat = models.IntegerField(default=0, null=True, blank=True, verbose_name='Location Latitude')
    location_lng = models.IntegerField(default=0, null=True, blank=True, verbose_name='Location Longitude')
    avatar = models.ImageField(upload_to='avatar_user/', null=True, blank=True, verbose_name='Avatar User')
    is_varified = models.BooleanField(default=False)


class CustomUserImage(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='User Identity', related_name='images')
    image = models.ImageField(upload_to='user_images/', null=True, blank=True, verbose_name='User Images')

    def __str__(self):
        return f'{self.user_id}'

    class Meta:
        verbose_name = "Custom User Image"
        verbose_name_plural = "Custom User Images"


