from django.contrib import admin

from polls.models import Answer, Poll, Possibility


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'poll_type', 'closes', 'public', 'active']
    date_hiearchy = 'created_on'
    search_fields = ['question', 'thread__title']
    actions = ['activate', 'deactivate']
    
    def activate(self, request, queryset):
        queryset.update(active=True)
    
    def deactivate(self, request, queryset):
        queryset.update(active=False)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['poll', 'user', 'created_on']
    filter_horizontal = ['possibilities']
    date_hiearchy = 'created_on'


@admin.register(Possibility)
class PossibilitiesAdmin(admin.ModelAdmin):
    list_display = ['poll', 'text']
    date_hiearchy = 'created_on'
    search_field = ['text', 'poll__question', 'poll__thread__title']
    list_per_page = 50
