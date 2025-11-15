from django.urls import re_path

from notifications.api import views

app_name = 'notifications'

urlpatterns = [
    re_path(
        r'^$',
        views.NotificationApi.as_view(),
        name='list'
    )
]
