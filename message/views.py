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


class MessageListView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    def get(self, request):
        queryset = MessageUsers.objects.filter(user = request.user).order_by('-id')
        serializers = MessageDetailSerializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = MessageUserListSerializer(data=request.data, partial=True, context={'user':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMsg(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]


    def post(self, request, id):
        get_filter_queryset = get_object_or_404(MessageUsers, id =id)
        serializers = CreateMsgSerializer(data=request.data, partial=True, context={'user':request.user, 'msg':get_filter_queryset, 'files':request.FILES.get('files', None)})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageUserDetailView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    def get(self, request, id):
        get_filter_queryset = MessagesRead.objects.filter(msg = id).order_by('date__minute')
        serializers = CreateMsgSerializer(get_filter_queryset, many=True)
        return Response(serializers.data, status= status.HTTP_200_OK)

class MessageReadDeatilView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    def delete(self, request, id):
        queryset = get_object_or_404(MessagesRead, id=id).delete()
        return Response({'msg':'Messages deleted successfully'})