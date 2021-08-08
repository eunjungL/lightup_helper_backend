from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from lightup.models import UserInfo
from chat.models import Message
from lightup_restAPI.serializers import UserInfoSerializer, LoginSerializer, MessageSerializer


class UserInfoViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = LoginSerializer


class ChatViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
