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
from haversine import haversine


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

    def get_queryset(self):
        user = self.queryset.get(user=self.request.user)

        user_lat, user_long = user.location.split(',')
        user_lat = float(user_lat)
        user_long = float(user_long)

        in_500 = []
        for other in self.queryset:
            if other.user == user.user:
                continue

            lat, long = other.location.split(',')
            lat = float(lat)
            long = float(long)

            if haversine((user_lat, user_long), (lat, long), unit='m') < 500:
                print(haversine((user_lat, user_long), (lat, long), unit='m'))
                in_500.append(other)

        print(in_500)

        return in_500


class UserLocationUpdateView(generics.UpdateAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer

    def partial_update(self, request, *args, **kwargs):
        queryset = self.queryset.get(user=self.request.user)
        serializer = self.serializer_class(queryset, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)


# Donation
class DonationViewSet(ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class DonationUserViewSet(ModelViewSet):
    queryset = DonationUser.objects.all()
    serializer_class = DonationUserSerializer


class DonationCommentViewSet(ModelViewSet):
    queryset = DonationComment.objects.all()
    serializer_class = DonationCommentSerializer


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
