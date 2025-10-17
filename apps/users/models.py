from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    커스텀 사용자 모델
    Django의 기본 User 모델을 확장하여 추가 필드를 포함합니다.
    """
    email = models.EmailField(unique=True, verbose_name="이메일")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self):
        return self.username
