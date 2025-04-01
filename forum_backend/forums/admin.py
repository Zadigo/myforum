from django.contrib import admin

from forums.models import Forum


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['title', 'admin', 'active']
    search_fields = ['title']
    date_hierarchy = 'created_on'
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(active=True)

    def deactivate(self, request, queryset):
        queryset.update(active=False)
