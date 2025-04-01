from django.db import models

class PollType(models.Choices):
    SINGLE = 'Single'
    MULTIPLE = 'Multiple'
    LIMITED  = 'Limited'
