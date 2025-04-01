from django.urls import re_path

from comments import views

app_name = 'comments'

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/bookmark', views.bookmark_comment_view),
    re_path(r'^(?P<pk>\d+)/delete', views.update_view),
    re_path(r'^(?P<pk>\d+)/update', views.update_view),
    re_path(r'^latest-comments$', views.latest_comments_view),
    re_path(r'^whats-new', views.whats_new_view),
    re_path(r'^create$', views.create_view)
]
