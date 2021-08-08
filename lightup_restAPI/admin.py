from django.contrib import admin
from lightup.models import UserInfo
from chat.models import Message

admin.site.register(UserInfo)
admin.site.register(Message)