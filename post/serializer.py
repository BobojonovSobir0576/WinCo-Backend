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
from authentification.serializers import UserProfileSerializer

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ['id','image']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    image = PostImageSerializer(read_only=True, many=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Post
        fields = ['image', 'uploaded_images','id', 'user','likes' ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")

        create = Post.objects.create(**validated_data)
        create.user = self.context.get('user')
        create.save()
        for item in uploaded_images:
            PostImage.objects.create(post=create, image=item)

        return create