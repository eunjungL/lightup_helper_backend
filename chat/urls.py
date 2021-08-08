from django.urls import path

from chat import views
from lightup_restAPI.views import ChatViewSet

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', ChatViewSet.as_view({
        'get': 'list', 'post': 'create'
    }), name='room'),
]