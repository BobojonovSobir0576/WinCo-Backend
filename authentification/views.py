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

        Util.send(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
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
            print(user)
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
    def get(self,request,format=None):
        try:
            serializers = self.serializers(request.user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as indetifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as indetifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':serializers.data},status=status.HTTP_200_OK)



class UserDetailView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    serializers = RegisterByEmailSerializer

    def put(self, request):
        serializers = self.serializers(instance=request.user, data=request.data, partial=True, context={'avatar':request.FILES.get('avatar', None)})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        queryset = CustomUser.objects.filter(id = request.user).first().delete()
        return Response({'message': 'deleted successfully'}, status=status.HTTP_200_OK)


class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)

        email = request.data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://' + current_site + relativeLink
            email_body = f'Hi \n Use link below to reset password \n link: {absurl}'
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your password'
            }

            Util.send(data)
        return Response({'success':'We have sent you to rest your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, Please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'msg':'Credential Valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, Please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'success'}, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

