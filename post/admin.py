from django.contrib import admin
from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id','post','image']
