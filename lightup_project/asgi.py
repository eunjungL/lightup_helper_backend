"""
ASGI config for lightup_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.channelsmiddleware import TokenAuthMiddleWare
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lightup_project.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleWare(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
