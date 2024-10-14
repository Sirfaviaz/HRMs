# chat/middleware.py
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
    except User.DoesNotExist:
        print("User does not exist")
    return None

class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to use JWT for WebSocket authentication.
    """

    async def __call__(self, scope, receive, send):
        # Get the JWT token from the query string or headers
        headers = dict(scope["headers"])
        query_string = scope.get("query_string", b"").decode()

        # Extract token from the header or query parameter
        token = None
        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode().split()
            if len(auth_header) == 2 and auth_header[0].lower() == "bearer":
                token = auth_header[1]
        elif "token" in query_string:
            token = query_string.split("token=")[-1]

        if token:
            user = await get_user(token)
            if user is not None:
                scope["user"] = user
            else:
                scope["user"] = None
        else:
            scope["user"] = None

        return await super().__call__(scope, receive, send)
