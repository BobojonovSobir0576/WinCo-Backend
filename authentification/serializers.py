from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


from .models import *
from .utils import *
import pdb


class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        modal = Group
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    groups = RolesSerializer(read_only=True, many=True)
    gender_id = GenderSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'age', 'username', 'email', 'gender_id', 'about_me', 'interests',
                  'location_lat', 'location_lng', 'avatar', 'password','groups']


class CustomUserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserImage
        field = ['id', 'user_id', 'image']


class RegisterByEmailSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=255, write_only=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','age','username','email','gender_id','about_me','interests','location_lat','location_lng','avatar','password','uploaded_images','images']
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'gender_id': {'write_only': True}
        }

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

        create = CustomUser.objects.create_user(**validated_data)
        create.avatar = self.context.get('avatar')
        create.save()

        return create

    def update(self, instance, validated_data):
        instance.model_method()
        update = super().update(instance,validated_data)
        update.avatar = self.context.get('avatar')
        update.save()
        return update

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        read_only_fields = ('username',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email',]


class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Invalid link', 401)

            user.set_password(password)
            user.save()
            print('success')
            return user
        except Exception:
            raise AuthenticationFailed('Invalid link', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')



