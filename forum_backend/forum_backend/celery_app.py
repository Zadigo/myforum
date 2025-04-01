import os

from celery import Celery
from celery.schedules import crontab
from comments.models import Comment
from threads.models import SubThread
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_backend.settings')


def get_broker():
    from django.conf import settings
    return getattr(settings, 'CELERY_BROKER_URL')


def get_backend():
    from django.conf import settings
    return getattr(settings, 'CELERY_RESULT_BACKEND')


app = Celery(
    'forum_backend',
    broker=get_broker(),
    backend=get_backend(),
    logger='celery_app.log'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/London',
    enable_utc=True,
    # task_routes={
    #     'emailing_script.tasks.testing': {
    #         'queue': 'seo'
    #     }
    # }
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'gather-statistics': {
        'task': 'gather_statistics',
        'schedule': crontab(day_of_week='mon', day_of_month=30, hour=6)
    },
    'unban-users': {
        'task': 'unban_users',
        'schedule': crontab(day_of_week='mon-wed-fri-sun', hour=6)
    },
    'ban-users': {
        'task': 'unban_users',
        'schedule': crontab(day_of_week='mon-wed-fri-sun', hour=5)
    },
    'publish-scheduled-comments': {
        'task': 'publish_scheduled_comments',
        'schedule': crontab(day_of_week='mon-wed-fri-sun', hour=7)
    },
    'publish-scheduled-threads': {
        'task': 'publish_scheduled_threads',
        'schedule': crontab(day_of_week='*', hour=8)
    },
}


@app.task(queue='statistics', ignore_result=True)
def gather_statistics():
    return NotImplemented


@app.task(queue='moderation', ignore_result=True)
def unban_users():
    return NotImplemented


@app.task(queue='moderation', ignore_result=True)
def ban_users():
    return NotImplemented


@app.task(queue='publication')
def publish_scheduled_comments():
    comments = Comment.objects.filter(pulish_on_isnone=False, published=False)
    if comments.exists():
        current_date = timezone.now()
        qs = comments.filter(publish_on=current_date)
        qs.update(published=True)


@app.task(queue='publication')
def publish_scheduled_threads():
    return NotImplemented
