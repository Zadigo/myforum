from django.db import models


class ThreadCategories(models.Choices):
    GENERAL_DISCUSSION = 'General discussion'
    BOMBSHELL = 'Bombshell'
    RESULT = 'Result'
    WWW = 'WWW'
    DRAW = 'Draw'
    POLL = 'Poll'


class ForumCategories(models.Choices):
    GENERAL = 'General'
    NEWS = 'News'
    MISCELLANEOUS = 'Miscellaneous'
    