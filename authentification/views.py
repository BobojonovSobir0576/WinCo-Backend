from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import *
from datetime import date, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
from .utils import *
from .renderers import UserRenderers

import jwt


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'accsess': str(refresh.access_token)
    }

class RegisteByEmailView(generics.GenericAPIView):
    serializer_class = RegisterByEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = CustomUser.objects.get(email=serializer.data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = f'Hi {user.username} Use link below to verify your email \n link: {absurl}'
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email'
        }

        Util.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])

            if not user.is_varified:
                user.is_varified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    username_param_config = openapi.Parameter('username', in_=openapi.IN_QUERY, description='Description',type=openapi.TYPE_STRING)
    password_param_config = openapi.Parameter('password', in_=openapi.IN_QUERY, description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[username_param_config, password_param_config])
    def post(self,request,format=None):
        serializers = LoginSerializer(data=request.data, partial=True)
        if serializers.is_valid(raise_exception=True):
            username = request.data.get('username','')
            password = request.data.get('password','')
            print(username)
            print(password)
            if username == '' and password == '':
                return Response({'error':{'none_filed_error':['Username or password is not write']}},status=status.HTTP_204_NO_CONTENT)
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error':('Invalid credentials, try again')}, status=status.HTTP_400_BAD_REQUEST)
            if not user.is_varified:
                return Response({'error':('Email is not varified')}, status=status.HTTP_400_BAD_REQUEST)
            token = get_token_for_user(user)
            return Response({'token':token},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    serializers = UserProfileSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request,format=None):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
            serializers = self.serializers(user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


