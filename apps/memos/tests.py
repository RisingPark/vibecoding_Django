from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.memos.models import Memo

User = get_user_model()


class SecurityTestCase(TestCase):
    """
    보안 테스트
    """

    def setUp(self):
        """테스트 사용자 및 클라이언트 설정"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!@#"
        )

    def test_csrf_protection_on_register(self):
        """회원가입 폼에 CSRF 보호가 있는지 테스트"""
        response = self.client.get(reverse("register"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_csrf_protection_on_login(self):
        """로그인 폼에 CSRF 보호가 있는지 테스트"""
        response = self.client.get(reverse("login"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_xss_protection_in_memo_content(self):
        """메모 내용에 XSS 보호가 있는지 테스트"""
        self.client.login(username="testuser", password="TestPass123!@#")
        
        # XSS 공격 시도
        xss_content = "<script>alert('XSS')</script>"
        memo = Memo.objects.create(
            user=self.user,
            title="Test Memo",
            content=xss_content
        )
        
        response = self.client.get(reverse("memo_detail", kwargs={"pk": memo.pk}))
        # Django가 자동으로 이스케이프하므로 스크립트 태그가 그대로 표시되어야 함
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert", html=False)

    def test_unauthorized_access_to_memo(self):
        """다른 사용자의 메모에 접근할 수 없는지 테스트"""
        # 다른 사용자 생성
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="OtherPass123!@#"
        )
        
        # 다른 사용자의 메모 생성
        memo = Memo.objects.create(
            user=other_user,
            title="Other's Memo",
            content="This is private"
        )
        
        # 첫 번째 사용자로 로그인
        self.client.login(username="testuser", password="TestPass123!@#")
        
        # 다른 사용자의 메모에 접근 시도
        response = self.client.get(reverse("memo_detail", kwargs={"pk": memo.pk}))
        self.assertEqual(response.status_code, 404)

    def test_password_validation_minimum_length(self):
        """비밀번호 최소 길이 검증 테스트"""
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "short",
            "password2": "short"
        })
        # 비밀번호가 너무 짧으면 회원가입 실패
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "password2",
            "이 비밀번호는 너무 짧습니다. 최소 8자 이상이어야 합니다."
        )

    def test_password_validation_common_password(self):
        """일반적인 비밀번호 차단 테스트"""
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "password",
            "password2": "password"
        })
        # 일반적인 비밀번호는 차단되어야 함
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "password2",
            "너무 흔히 사용되는 비밀번호입니다."
        )

    def test_login_required_for_memo_operations(self):
        """메모 작업에 로그인이 필요한지 테스트"""
        # 로그인하지 않고 메모 목록에 접근
        response = self.client.get(reverse("memo_list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn("/login/", response.url)
        
        # 로그인하지 않고 메모 생성에 접근
        response = self.client.get(reverse("memo_create"))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn("/login/", response.url)

    def test_sql_injection_protection(self):
        """SQL Injection 보호 테스트"""
        self.client.login(username="testuser", password="TestPass123!@#")
        
        # SQL Injection 시도
        sql_injection = "'; DROP TABLE memos; --"
        memo = Memo.objects.create(
            user=self.user,
            title=sql_injection,
            content="Test content"
        )
        
        # Django ORM이 SQL Injection을 방지하므로 메모가 정상적으로 저장되어야 함
        saved_memo = Memo.objects.get(pk=memo.pk)
        self.assertEqual(saved_memo.title, sql_injection)
        
        # 메모 테이블이 여전히 존재하는지 확인
        self.assertTrue(Memo.objects.exists())

    def test_session_security_after_logout(self):
        """로그아웃 후 세션이 무효화되는지 테스트"""
        # 로그인
        self.client.login(username="testuser", password="TestPass123!@#")
        
        # 로그인 상태 확인
        response = self.client.get(reverse("memo_list"))
        self.assertEqual(response.status_code, 200)
        
        # 로그아웃
        self.client.logout()
        
        # 로그아웃 후 메모 목록 접근 시 로그인 페이지로 리다이렉트
        response = self.client.get(reverse("memo_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

