from django.urls import re_path

from forums.api import views

app_name = 'forums_api'

urlpatterns = [
    re_path(r'^(?P<pk>\d+)$', views.forum_threads_view),
    re_path(r'^$', views.forums_view)
]
