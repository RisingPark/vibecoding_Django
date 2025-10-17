from django import forms
from .models import Memo


class MemoForm(forms.ModelForm):
    """
    메모 작성/수정 폼
    제목과 내용을 입력받습니다.
    """
    class Meta:
        model = Memo
        fields = ["title", "content"]
        labels = {
            "title": "제목",
            "content": "내용",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "메모 제목을 입력하세요"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 10,
                "placeholder": "메모 내용을 입력하세요"
            }),
        }
