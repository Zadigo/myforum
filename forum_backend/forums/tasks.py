from celery import shared_task

@shared_task
def gather_statistics():
    return NotImplemented
