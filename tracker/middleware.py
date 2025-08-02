import jwt
from urllib.parse import parse_qs
from django.conf import settings
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(user_id):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser

    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = self.scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")
                self.scope["user"] = await get_user(user_id)
            except jwt.ExpiredSignatureError:
                from django.contrib.auth.models import AnonymousUser
                self.scope["user"] = AnonymousUser()
            except jwt.InvalidTokenError:
                from django.contrib.auth.models import AnonymousUser
                self.scope["user"] = AnonymousUser()
        else:
            from django.contrib.auth.models import AnonymousUser
            self.scope["user"] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)
