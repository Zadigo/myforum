from celery import shared_task
from celery.utils.log import get_task_logger
from comments.models import Comment
from django.contrib.auth import get_user_model
from notifications.models import Notification
from threads.models import MainThread

logger = get_task_logger(__name__)


@shared_task
def create_notifications(**kwargs: dict[str, str | int]):
    # Message, Follow, Like, Shoutout
    user_ids = kwargs['user_ids']
    comment_id = kwargs.get('comment', None)

    comment = None

    if comment_id is not None:
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            logger.error('Comment does not exist')

    users = get_user_model().objects.filter(id__in=user_ids)
    # Only notify active users -; banned users
    # however can still be mentionned or notified
    active_users = users.filter(is_active=True)

    for user in active_users:
        Notification.objects.create(**{
            'user': user,
            'message': comment,
            'notification_type': kwargs['notification_type']
        })

    logger.warning(f"Created notifications for users: {user_ids}")
    return user_ids


@shared_task
def create_message_notifications(comment_id: int, user_ids: list[int]):
    create_notifications.apply_async(kwargs={
        'comment': comment_id,
        'user_ids': user_ids,
        'notification_type': 'Message'
    })
    return user_ids


@shared_task
def create_thread_followers_notifications(thread_id: int):
    """Notify the users following a given thread that an
    event has occured in a thread"""
    try:
        instance = MainThread.objects.get(id=thread_id)
    except:
        logger.error('Thread does not exist')
        return
    else:
        user_ids = instance.followers.values_list('id', flat=True)
        create_notifications.apply_async(kwargs={
            'user_ids': list(user_ids),
            'notification_type': 'Message'
        })
