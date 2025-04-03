from celery import shared_task
from celery.utils.log import get_logger
from comments.models import Comment
from django.contrib.auth import get_user_model
from notifications.models import Notification

logger = get_logger('comments')


@shared_task
def create_notifications(data: dict[str, str | int]):
    # Message, Follow, Like, Shoutout
    user_ids = data['user_ids']
    comment_id = data.get('comment', None)

    comment = None

    if comment_id is not None:
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            logger.error('Comment does not exist')

    users = get_user_model().objects.filter(id__in=user_ids)
    # Only notify active users -; banned users
    # however can still be mentionned or notified
    active_users = users.filte(active=True)

    for user in active_users:
        Notification.objects.create(**{
            'user': user,
            'message': comment,
            'notification_type': data['notification_type']
        })

    return user_ids


@shared_task
def create_message_notifications(comment_id: int, user_ids: list[int]):
    create_notifications.apply_async(kwargs={
        'comment': comment_id,
        'user_ids': user_ids,
        'notification_type': 'Message'
    })
    return user_ids
