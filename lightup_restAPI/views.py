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

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# kakao login
def kakao_login(request):
    rest_api_key = '98bcbd28d1569d2e928917f853eb03b9'
    kakao_callback_uri = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'
    kakao_callback_uri_release = 'http://3.38.51.117:8000/accounts/kakao/login/callback/'
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={kakao_callback_uri_release}&response_type=code"
    )


def kakao_callback(request):
    rest_api_key = '98bcbd28d1569d2e928917f853eb03b9'
    kakao_callback_uri = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'
    kakao_callback_uri_release = 'http://3.38.51.117:8000/accounts/kakao/login/callback/'
    code = request.GET.get('code')

    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={kakao_callback_uri_release}&code={code}"
    )
    token_request_json = token_request.json()
    access_token = token_request_json.get('access_token')

    gender_request = requests.get(
        f"https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    gender_json = gender_request.json()
    kakao_account = gender_json.get('kakao_account')
    print(kakao_account.get('gender'))

    if kakao_account.get('gender') == 'female':
        return JsonResponse({"check": True})
    else:
        return JsonResponse({"check": False})


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

            print(other)

            lat, long = other.location.split(',')
            lat = float(lat)
            long = float(long)

            if haversine((user_lat, user_long), (lat, long), unit='m') < 500:
                print(haversine((user_lat, user_long), (lat, long), unit='m'))
                in_500.append(other)

        print(in_500)

        return in_500


class UserLocationGetView(generics.ListAPIView):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


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


class DonationLikeView(generics.UpdateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def partial_update(self, request, *args, **kwargs):
        queryset = self.queryset.get(title=self.request.data['notice_title'])

        if self.request.user in queryset.like.all():
            queryset.like.remove(self.request.user)
        else:
            queryset.like.add(self.request.user)

        queryset.save()

        return response.Response(self.serializer_class(queryset).data)


class DonationLikeListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def get_queryset(self):
        return self.queryset.filter(like=self.request.user)


class DonationUserViewSet(ModelViewSet):
    queryset = DonationUser.objects.all()
    serializer_class = DonationUserSerializer


class DonationCommentViewSet(ModelViewSet):
    queryset = DonationComment.objects.all()
    serializer_class = DonationCommentSerializer

    def get_queryset(self):
        donation_id = self.request.query_params.get('id')
        donation = Donation.objects.get(id=donation_id)

        return self.queryset.filter(item=donation)


# Borrow
class BorrowStateViewSet(ModelViewSet):
    queryset = BorrowState.objects.all()
    serializer_class = BorrowStateSerializer


class BorrowStateLendGetView(generics.ListAPIView):
    queryset = BorrowState.objects.all()
    serializer_class = BorrowStateSerializer

    def get_queryset(self):
        return self.queryset.filter(lender=self.request.user)


class BorrowStateBorrowGetView(generics.ListAPIView):
    queryset = BorrowState.objects.all()
    serializer_class = BorrowStateSerializer

    def get_queryset(self):
        return self.queryset.filter(borrower=self.request.user)


# Community
class CommunityPostViewSet(ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer


class CommunityPostLikeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

    def partial_update(self, request, *args, **kwargs):
        post = self.queryset.get(id=self.request.data['id'])

        if self.request.user in post.like.all():
            post.like.remove(self.request.user)
        else:
            post.like.add(self.request.user)

        post.save()

        return response.Response(self.serializer_class(post).data)


class CommunityCommentViewSet(ModelViewSet):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityCommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('id')
        post = CommunityPost.objects.get(id=post_id)

        return self.queryset.filter(post=post)


class CommunityCommentLikeView(generics.UpdateAPIView):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityCommentSerializer

    def partial_update(self, request, *args, **kwargs):
        comment = self.queryset.get(id=self.request.data['id'])

        if self.request.user in comment.like.all():
            comment.like.remove(self.request.user)
        else:
            comment.like.add(self.request.user)

        comment.save()

        return response.Response(self.serializer_class(comment).data)


# Chat
class ChatViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.request.query_params.get('room')

        return self.queryset.filter(room=room_name)


class ChatCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
