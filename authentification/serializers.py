from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib import auth

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

from .models import *


class RegisterByEmailSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=255, write_only=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return super().validate(attrs)

    def validate_email(self, value):
        email = value.lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already exits ..")
        return email

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=50, min_length=3)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        read_only_fields = ('username',)

