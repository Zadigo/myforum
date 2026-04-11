import enum

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
    

class OrderingMethods(enum.Enum):
    AZ = 'Sort alphabetically A-Z'
    ZA = 'Sort alphabetically Z-A'
    MOST_RECENT = 'Most recent'
    NUMBER_OF_COMMENTS = 'Number of comments'
