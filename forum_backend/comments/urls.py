from django.urls import re_path

from comments.api import views

app_name = 'comments'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/bookmark$',
        views.BookmarkComment.as_view(),
        name='bookmark'
    ),
    re_path(
        r'^(?P<pk>\d+)/reply$',
        views.GetUpdateDeleteComment.as_view(),
        name='get_update_delete_comment'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        views.GetUpdateDeleteComment.as_view(),
        name='get_update_delete_comment'
    ),
    re_path(
        r'^latest$',
        views.LatestComments.as_view(),
        name='latest_comments'
    ),
    re_path(
        r'^whats-new',
        views.whats_new_view
    ),
    re_path(
        r'^create$',
        views.CreateComment.as_view(),
        name='create'
    )
]
