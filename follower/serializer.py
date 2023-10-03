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

class FollowerSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    followed_by = UserProfileSerializer(read_only=True)
    get_lists = serializers.ListField(
    child = serializers.IntegerField(min_value = 0, max_value = 100), write_only=
    True
    )

    class Meta:
        model = Follower
        fields = ['id', 'user', 'followed_by','get_lists']


    def create(self, validated_data):
        get_lists = validated_data.pop("get_lists")
        create = Follower.objects.create(**validated_data)
        for list in get_lists:
            get_queryset = CustomUser.objects.filter(id = list).first()
            create.followed_by = get_queryset
            create.user = self.context.get('user')
            create.save()
        return create

    