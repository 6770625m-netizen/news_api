from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_blocked', 'blocked_until', 'is_active']
    list_filter = ['role', 'is_blocked', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol va Bloklash', {
            'fields': ('role', 'bio', 'avatar', 'is_blocked', 'blocked_until', 'block_reason')
        }),
    )
    # Admin panelda rol tanlashda barcha rollar ko'rinadi (admin qo'lda belgilaydi)
    readonly_fields = ['created_at', 'updated_at'] if hasattr(User, 'created_at') else []
