from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    """
    회원가입 뷰
    GET: 회원가입 폼 표시
    POST: 회원가입 처리
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"{username}님, 회원가입이 완료되었습니다! 로그인해주세요.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form, "title": "회원가입"})


def home(request):
    """
    홈페이지 뷰
    """
    return render(request, "home.html", {"title": "메모짱"})
