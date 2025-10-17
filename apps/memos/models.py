from django.db import models
from django.conf import settings


class Memo(models.Model):
    """
    메모 모델
    사용자가 작성한 메모를 저장합니다.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memos",
        verbose_name="작성자"
    )
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "메모"
        verbose_name_plural = "메모 목록"

    def __str__(self):
        return self.title
