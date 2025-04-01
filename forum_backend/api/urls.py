from django.urls import re_path
from rest_framework.routers import DefaultRouter

from api.views import comments, reports, search, forums, users

app_name = 'api'

router = DefaultRouter()
# router.register('comments', comments.CommentsView)
# router.register('forums', forums.ForumsView)
router.register('reports', reports.ReportView)
router.register('threads', forums.ThreadsView)


urlpatterns = [
    # re_path(r'^forums/(?P<pk>\d+)/threads', forums.forum_threads_view),
    
    # re_path(r'^threads/(?P<pk>\d+)/comments', comments.comments_view),
    
    # re_path(r'^comments/(?P<pk>\d+)/bookmark', comments.bookmark_comment_view),
    
    # re_path(r'^users', users.get_users),
    # re_path(r'^search', search.search)
    
    # url(r'^threads/(?P<pk>\d+)/sub-thread/create$', comments_views.thread_comments_view),
    # re_path(r'^threads/(?P<pk>\d+)/comments/(?P<comment_id>\d+)$', comments_views.thread_comments_view),
    # re_path(r'^threads/(?P<pk>\d+)/comments$', comments_views.thread_comments_view),

    # re_path(r'^comments/(?P<pk>\d+)/save$', comments_views.save_comment),



    # re_path(r'^threads/(?P<pk>\d+)/', include((comments, app_name))),
    # path(r'notifictations', include((app_name, notifications)), name='api_notifictations'),
    # path(r'threads', include((app_name, threads)), name='api_threads'),
    # path(r'subthreads', include((app_name, subthreads)), name='api_subthreads'),
]

urlpatterns.extend(router.urls)
