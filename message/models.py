from django.db import models
from authentification.models import CustomUser


class MessageUsers(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='msg_user', null=True, blank=True)
    followed_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='msg_followed_by', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class MessagesRead(models.Model):
    msg = models.ForeignKey(MessageUsers, on_delete=models.CASCADE, related_name='msg', null=True, blank=True)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='attachment', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)