from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

user_model = get_user_model()


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        # Validate the token
        access_token = AccessToken(token_key)
        user_id = access_token['user_id']

        # Get the user
        user = user_model.objects.get(id=user_id)
        return user
    except (InvalidToken, TokenError, user_model.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that authenticates users via JWT token in WebSocket connections
    """

    async def __call__(self, scope, receive, send):
        # Get the token from query string
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        # If no token in query string, check headers (for some clients)
        if not token:
            headers = dict(scope.get('headers', []))
            auth_header = headers.get(b'authorization', b'').decode()

            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if token:
            # Authenticate user
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
