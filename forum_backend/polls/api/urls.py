from django.urls import re_path

from polls.api import views

app_name = 'polls_api'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/answers$',
        views.GetPollAnswers.as_view(),
        name='answers'
    ),
    re_path(
        r'^(?P<pk>\d+)/answer$',
        views.AnswerPoll.as_view(),
        name='answer_poll'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        views.GetPoll.as_view(),
        name='poll'
    )
]
