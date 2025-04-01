from django.db import models


class ForumCategories(models.Choices):
    """The global categories for the forums
    in the dabase"""

    GENERAL = 'General'
    NEWS = 'News'
    MISCELLANEOUS = 'Miscellaneous'
