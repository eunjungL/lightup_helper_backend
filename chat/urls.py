from django.urls import path

from chat import views
from lightup_restAPI.views import ChatViewSet, ChatCreateView

urlpatterns = [
    path('', ChatViewSet.as_view({
        'get': 'list'
    }), name='index'),
    path('<str:room_name>/', ChatCreateView.as_view(), name='room'),
]