from typing import Iterator

from celery import group, shared_task
from celery.utils.log import get_task_logger
from comments.models import Comment
from django.contrib.auth import get_user_model
from moderation.tasks import create_report
from nltk.tokenize import TweetTokenizer
from notifications import tasks as notification_tasks
from tags.models import Tag

logger = get_task_logger(__name__)


@shared_task
def moderate_comment(comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    logger.warning(f"Moderating comment {comment_id}")

    # moderate = lambda x: False

    # result = moderate(comment.content)
    # if result:
    #     # Create a report for the comment
    #     create_report.delay(
    #         thread_id=comment.thread.id,
    #         reason='Auto-moderation triggered',
    #         reporter_id=None
    #     )
    # return result


@shared_task
def analyze_comment_with_ai(comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    logger.warning(f"Analyzing comment {comment_id} with AI")


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
    hashtags: list[str] = list(
        map(
            lambda x: x.replace('#', '').strip(),
            filter(lambda x: x.startswith('#'), tokens)
        )
    )

    users = get_user_model().objects.filter(username__in=list(mentions))
    user_ids = list(users.values_list('id', flat=True))

    notification_tasks.create_message_notifications.apply_async(
        args=[
            comment_id,
            user_ids
        ],
        countdown=40
    )

    if users.exists():
        logger.warning(f"Comment {comment_id} mentionned users: {len(user_ids)}")

    for hashtag in hashtags:
        instance, state = Tag.objects.get_or_create(name=hashtag)

    if hashtags:
        logger.warning(f"Comment {comment_id} has hashtags: {len(hashtags)}")
