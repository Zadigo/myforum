from django.urls.conf import re_path

from threads.api import views

app_name = 'threads_api'

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/comments$', views.paginated_comments_view),
    re_path(r'^(?P<pk>\d+)/follow$', views.follow_thread),
    re_path(r'^(?P<pk>\d+)/delete$', views.delete_view),
    re_path(r'^(?P<pk>\d+)/update$', views.update_view),
    re_path(
        r'^create$', 
        views.CreateThread.as_view(), 
        name='create'
    )
    # re_path(r'^create$', views.create_view)
]
