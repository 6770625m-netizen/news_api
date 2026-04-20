from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'news', 'created_at']
    search_fields = ['author__username', 'news__title']
    list_filter = ['created_at']
