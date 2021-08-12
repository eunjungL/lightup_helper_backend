from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
import requests
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


# kakao login
def kakao_login(request):
    rest_api_key = '98bcbd28d1569d2e928917f853eb03b9'
    KAKAO_CALLBACK_URI = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

def kakao_callback(request):
    rest_api_key = '98bcbd28d1569d2e928917f853eb03b9'
    KAKAO_CALLBACK_URI = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'
    code = request.GET.get('code')

    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )
    token_request_json = token_request.json()
    return JsonResponse(token_request_json)


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
