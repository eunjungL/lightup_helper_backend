from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.db import close_old_connections
import os
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from django.conf import settings
from channels.db import database_sync_to_async
from lightup.models import UserInfo


@database_sync_to_async
def get_user(id):
    return UserInfo.objects.get(user__id=id)


class TokenAuthMiddleWare:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        token = parse_qs(scope["query_string"].decode("utf-8"))["token"][0]
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            print(e)
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = await get_user(decoded_data['user_id'])
            scope['user'] = user

        return await self.inner(scope, receive, send)
