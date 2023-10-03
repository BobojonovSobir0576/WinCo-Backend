from django.contrib import admin
from .models import *

@admin.register(MessageUsers)
class MessageUsersAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'followed_by', 'date']

@admin.register(MessagesRead)
class MessagesReadAdmin(admin.ModelAdmin):
    list_display = ['id','sender', 'msg', 'date', 'text']