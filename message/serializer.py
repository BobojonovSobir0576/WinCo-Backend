from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


from .models import *
from authentification.serializers import *

class MessageUserListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = MessageUsers
        fields = ['id', 'user', 'followed_by', 'date']

    def create(self, validated_data):
        create = MessageUsers.objects.create(
            followed_by = validated_data['followed_by'],
            user = self.context.get('user')
        )
        return create


class MessageDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    followed_by = UserProfileSerializer(read_only=True)

    class Meta:
        model = MessageUsers
        fields = ['id', 'user', 'followed_by', 'date']


class CreateMsgSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    class Meta:
        model = MessagesRead
        fields  = ['id','msg', 'sender', 'text', 'attachment', 'date']

    def create(self, validated_data):
        print(self.context.get('msg'))
        print(self.context.get('user'))
        create = MessagesRead.objects.create(
            msg = self.context.get('msg'),
            sender = self.context.get('user'),
            text = validated_data['text'],
            attachment = self.context.get('files')
        )
        return create