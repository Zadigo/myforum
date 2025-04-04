from django.urls.conf import re_path

from threads.api import views

app_name = 'threads_api'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/comments$',
        views.ThreadComments.as_view(),
        name='comments'
    ),
    re_path(
        r'^(?P<pk>\d+)/follow$',
        views.FollowThread.as_view(),
        name='follow'
    ),
    re_path(
        r'^(?P<pk>\d+)/delete$',
        views.DeleteThread.as_view(),
        name='delete'
    ),
    re_path(
        r'^(?P<pk>\d+)/poll$',
        views.ThreadPoll.as_view(),
        name='poll'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        views.ThreadDetail.as_view(),
        name='detail_update'
    ),
    re_path(
        r'^create$',
        views.CreateThread.as_view(),
        name='create'
    )
]
