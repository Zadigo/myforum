from celery import shared_task

@shared_task
def schedule_thread():
    pass


@shared_task
def moderate_thread():
    pass


@shared_task
def analyze_thread():
    pass
