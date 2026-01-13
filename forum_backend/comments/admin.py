from django.contrib import admin
from comments.models import Comment, MediaContent, Quote, SavedComment, Reply


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_on', 'active']
    search_fields = ['user', 'title', 'content']
    ordering = ['-created_on']
    list_max_show_all = 10
    date_hierarchy = 'created_on'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_on', 'active']
    search_fields = ['user', 'content']
    ordering = ['-created_on']
    list_max_show_all = 10
    date_hierarchy = 'created_on'


@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    list_display = ['media_content_id', 'created_on']
    search_fields = ['content']
    list_max_show_all = 10
    date_hierarchy = 'created_on'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['comment', 'quoted_comment', 'created_on']
    search_fields = ['comment__user__username',
                     'quoted_comment__user__username', 'content']
    date_hierarchy = 'created_on'
    list_per_page = 10


@admin.register(SavedComment)
class SavedCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_on']
    search_fields = ['comment__title', 'comment__content', 'user__username']
    date_hierarchy = 'created_on'
