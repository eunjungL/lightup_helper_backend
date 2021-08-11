from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from lightup_restAPI.serializers import *
from rest_framework import generics, response


# User
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = LoginSerializer


class UserInfoViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class UserBorrowStateUpdateView(generics.UpdateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserBorrowStateUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        queryset = self.queryset.get(user=self.request.user)
        serializer = self.serializer_class(queryset, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)


class UserLocationViewSet(ModelViewSet):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer


class UserLocationUpdateView(generics.UpdateAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer

    def partial_update(self, request, *args, **kwargs):
        queryset = self.queryset.get(user__user=self.request.user)
        serializer = self.serializer_class(queryset, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)


# Borrow
class BorrowStateViewSet(ModelViewSet):
    queryset = BorrowState.objects.all()
    serializer_class = BorrowStateSerializer


# Chat
class ChatViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
