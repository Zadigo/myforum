from django.urls import re_path
from forums.api import views

app_name = 'forums_api'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/threads$',
        views.ForumThreads.as_view(),
        name='forum_threads'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        views.ForumDetails.as_view(),
        name='forum'
    ),
    re_path(
        r'^$',
        views.ListForums.as_view(),
        name='forums'
    )
]
