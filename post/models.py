from django.db import models
from authentification.models import *



class Post(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    likes = models.IntegerField(default=0, null=True, blank=True)

class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='image', null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)


