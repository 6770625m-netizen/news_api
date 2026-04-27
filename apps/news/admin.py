from django.contrib import admin
from .models import News, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'category']
    search_fields = ['title', 'author__username']

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if getattr(request.user, 'role', None) == 'journalist':
            initial['status'] = News.STATUS_PUBLISHED
        return initial

    def save_model(self, request, obj, form, change):
        if not change and getattr(request.user, 'role', None) == 'journalist':
            obj.status = News.STATUS_PUBLISHED
        super().save_model(request, obj, form, change)
