from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import *
from datetime import date, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serializer import *
from authentification.renderers import UserRenderers



class PostView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    serializers = PostSerializer

    def get(self, request):
        queryset = Post.objects.filter(user = request.user).all().order_by('-id')
        serializers = self.serializers(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = self.serializers(data=request.data, context={'user':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    serializers = PostSerializer

    def get(self, request, id):
        queryset = get_object_or_404(Post, id=id)
        queryset.likes = queryset.likes + 1
        queryset.save()
        serializers = self.serializers(queryset)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        queryset = get_object_or_404(Post, id=id).delete()
        return Response({'msg':'Successfully deleted'}, status=status.HTTP_202_ACCEPTED)

class PostLikeView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    serializers = PostSerializer

    def get(self, request, id):
        queryset = get_object_or_404(Post, id=id)
        queryset.likes = queryset.likes + 1
        queryset.save()
        serializers = self.serializers(queryset)
        return Response(serializers.data, status=status.HTTP_200_OK)


class PostUnlikeView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    serializers = PostSerializer

    def get(self, request, id):
        queryset = get_object_or_404(Post, id=id)
        queryset.likes = queryset.likes - 1
        queryset.save()
        serializers = self.serializers(queryset)
        return Response(serializers.data, status=status.HTTP_200_OK)