from django.db import models
from authentification.models import *

class Follower(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    followed_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followed_by', null=True, blank=True)

    # def __str__(self):
    #     return f"{str(self.user.first_name)} is followed by {str(self.followed_by)}"

    @staticmethod
    def followers_count(user):
        return Follower.objects.filter(user=user).all().count()

    @staticmethod
    def following_count(followed_by):
        return Follower.objects.filter(followed_by=followed_by).all().count()