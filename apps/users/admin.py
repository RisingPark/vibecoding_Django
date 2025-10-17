from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    사용자 관리자 설정
    """
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "date_joined"]
    list_filter = ["is_staff", "is_superuser", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ("추가 정보", {
            "fields": ("created_at", "updated_at")
        }),
    )
    
    readonly_fields = ["date_joined", "last_login", "created_at", "updated_at"]
