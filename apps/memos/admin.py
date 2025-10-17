from django.contrib import admin
from .models import Memo


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    """
    메모 관리자 설정
    """
    list_display = ["title", "user", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["title", "content", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("메모 정보", {
            "fields": ("user", "title", "content")
        }),
        ("날짜 정보", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
