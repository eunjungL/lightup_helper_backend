from django.contrib import admin
from django.apps import apps
from chat.models import Message

app = apps.get_app_config('lightup')

for name, model in app.models.items():
    print(model)
    admin.site.register(model)

admin.site.register(Message)

