from django.urls import re_path
from polls import views

app_name = 'polls'

urlpatterns = [
    re_path(r'^create$', views.create_view),
    re_path(r'^(?P<pk>\d+)/answer$', views.answer_poll_view),
    re_path(r'^(?P<pk>\d+)$', views.poll_view)
]
