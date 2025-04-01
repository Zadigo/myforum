from django.contrib import admin

from moderation.models import UserModerationPreference, Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_id', 'comment', 'thread', 'reviewed']
    date_hierarchy = 'created_on'
    search_fields = ['reference', 'comment__content',
                     'thread__title', 'reviewed_by__user__username']
    list_filter = ['reviewed']

    def mark_reviewed(self, request, queryset):
        queryset.update(reviewed=True, reviewed_by=request.user)


@admin.register(UserModerationPreference)
class UserModerationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_to_moderate']
    search_fields = ['user__username', 'user__user_to_moderate__username']
