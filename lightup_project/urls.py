"""lightup_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lightup_restAPI import views
from allauth import urls

router = DefaultRouter()
router.register(r'users', views.UserInfoViewSet)
router.register(r'user/location', views.UserLocationViewSet)
router.register(r'borrow', views.BorrowStateViewSet)
router.register(r'donation', views.DonationViewSet)
router.register(r'donation_user', views.DonationUserViewSet)
router.register(r'donation_comment', views.DonationCommentViewSet)
router.register(r'community_post', views.CommunityPostViewSet)
router.register(r'community_comment', views.CommunityCommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # app login (for app token)
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),

    # kakao login
    path('accounts/kakao/login/', views.kakao_login),
    path('accounts/kakao/login/callback/', views.kakao_callback),

    # chat
    path('chat/', include('chat.urls')),

    # user update
    path('update/borrowState/user/', views.UserBorrowStateUpdateView.as_view()),
    path('update/location/user/', views.UserLocationUpdateView.as_view()),

    # like
    path('like/donation/', views.DonationLikeView.as_view()),
    path('get/like/donation/', views.DonationLikeListView.as_view()),
    path('like/post/', views.CommunityPostLikeView.as_view()),

]
