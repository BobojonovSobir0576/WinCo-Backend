from django.contrib import admin
from .models import *



@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'followed_by']