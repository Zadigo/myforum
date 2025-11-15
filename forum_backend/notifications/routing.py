from django.urls import re_path
from notifications import consumers


ws_urlpatterns = [
    re_path(
        r'ws/notifications$',
        consumers.NotificationConsumer.as_asgi()
    )
]
