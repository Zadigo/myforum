from celery import shared_task, group
from moderation.models import Report

@shared_task
def create_report(thread_id: int, reason: str, reporter_id: int):
    report = Report.objects.create(
        thread_id=thread_id,
        reason=reason,
        reporter_id=reporter_id
    )
    return report.id
