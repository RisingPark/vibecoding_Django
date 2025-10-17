from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Memo
from .forms import MemoForm


@login_required
def memo_list(request):
    """
    메모 목록 조회
    로그인한 사용자의 메모만 표시합니다.
    """
    memos = Memo.objects.filter(user=request.user)
    return render(request, "memos/memo_list.html", {
        "memos": memos,
        "title": "내 메모"
    })


@login_required
def memo_create(request):
    """
    메모 생성
    POST: 메모 저장
    GET: 메모 작성 폼 표시
    """
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.save()
            messages.success(request, "메모가 성공적으로 작성되었습니다.")
            return redirect("memo_detail", pk=memo.pk)
    else:
        form = MemoForm()
    return render(request, "memos/memo_form.html", {
        "form": form,
        "title": "새 메모 작성",
        "button_text": "작성하기"
    })


@login_required
def memo_detail(request, pk):
    """
    메모 상세 조회
    본인의 메모만 조회 가능합니다.
    """
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    return render(request, "memos/memo_detail.html", {
        "memo": memo,
        "title": memo.title
    })


@login_required
def memo_update(request, pk):
    """
    메모 수정
    POST: 메모 업데이트
    GET: 메모 수정 폼 표시
    본인의 메모만 수정 가능합니다.
    """
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            messages.success(request, "메모가 성공적으로 수정되었습니다.")
            return redirect("memo_detail", pk=pk)
    else:
        form = MemoForm(instance=memo)
    return render(request, "memos/memo_form.html", {
        "form": form,
        "title": "메모 수정",
        "button_text": "수정하기"
    })


@login_required
def memo_delete(request, pk):
    """
    메모 삭제
    POST: 메모 삭제 실행
    GET: 삭제 확인 페이지 표시
    본인의 메모만 삭제 가능합니다.
    """
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        memo.delete()
        messages.success(request, "메모가 성공적으로 삭제되었습니다.")
        return redirect("memo_list")
    return render(request, "memos/memo_confirm_delete.html", {
        "memo": memo,
        "title": "메모 삭제"
    })
