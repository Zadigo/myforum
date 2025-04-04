from django.contrib import admin

from notifications import models


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'created_on']
    search = ['video__caption']
    date_hierarchy = 'created_on'
    list_per_page = 10
