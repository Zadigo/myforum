from typing import Iterator

from celery import shared_task, group
from django.contrib.auth import get_user_model
from nltk.tokenize import TweetTokenizer
from notifications import tasks as notification_tasks
from tags.models import Tag


@shared_task
def moderate_comment(text: str):
    pass


@shared_task
def analyze_comment_with_ai(text: str):
    pass


@shared_task
def analyze_comment(comment_id: int, text: str):
    """Extract the mentions so that we can eventually
    notify the users that were mentionned - also,
    save the hashtags"""
    instance = TweetTokenizer()
    tokens = instance.tokenize(text)

    # Map the mentions so that we can send
    # notifications to the people that were
    # mentionned
    mentions: Iterator[str] = map(
        lambda x: x.replace('@', '').strip(),
        filter(lambda x: x.startswith('@'), tokens)
    )
    hashtags: Iterator[str] = map(
        lambda x: x.replace('#', '').strip(),
        filter(lambda x: x.startswith('#'), tokens)
    )

    users = get_user_model().objects.filter(username__in=list(mentions))
    user_ids = list(users.values_list('id', flat=True))

    notification_tasks.create_message_notifications.apply_async(
        (
            comment_id,
            user_ids
        )
    )

    for hashtag in hashtags:
        instance, state = Tag.objects.get_or_create(name=hashtag)
