from django.urls.conf import re_path

from threads.api import views

app_name = 'threads_api'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/comments$',
        views.paginated_comments_view,
        name='comments'
    ),
    re_path(
        r'^(?P<pk>\d+)/follow$',
        views.follow_thread,
        name='follow'
    ),
    re_path(
        r'^(?P<pk>\d+)/delete$',
        views.delete_view,
        name='delete'
    ),
    re_path(
        r'^(?P<pk>\d+)/update$',
        views.update_view,
        name='update'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        views.ThreadDetail.as_view(),
        name='detail'
    ),
    re_path(
        r'^create$',
        views.CreateThread.as_view(),
        name='create'
    )
]
