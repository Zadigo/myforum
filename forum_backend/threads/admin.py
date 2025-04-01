from django.contrib import admin

from threads.models import MainThread, SubThread


@admin.register(MainThread)
class MainThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'active']
    search_fields = ['title', 'category', 'tags']
    list_max_show_all = 10
    date_hierarchy = 'created_on'
    actions = ['activate', 'deactivate', 'merge']

    def activate(self, request, queryset):
        queryset.update(active=True)

    def deactivate(self, request, queryset):
        queryset.update(active=False)

    def merge(self, request, queryset):
        for thread in queryset:
            pass


@admin.register(SubThread)
class SubThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_on']
    search_fields = ['title', 'category', 'tags']
    list_max_show_all = 10
    date_hierarchy = 'created_on'
