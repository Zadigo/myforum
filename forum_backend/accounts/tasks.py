from celery import shared_task


@shared_task
def login_workflow():
    return NotImplemented


@shared_task
def logout_workflow():
    return NotImplemented


@shared_task
def ban_user_workflow(user_id):
    return NotImplemented


@shared_task
def strike_user(user_id):
    return NotImplemented
