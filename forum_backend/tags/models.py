from django.db import models
from django.shortcuts import reverse

from tags import validators


class Tag(models.Model):
    """Represents a tag/hashtag for the given
    thread or forum"""

    name = models.CharField(
        max_length=30,
        unique=True,
        validators=[validators.tag_name_validator]
    )
    created_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tags:tag', args=[self.title])
