from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSecurityTestCase(TestCase):
    """
    사용자 보안 테스트
    """

    def setUp(self):
        """테스트 클라이언트 설정"""
        self.client = Client()

    def test_password_hashing(self):
        """비밀번호가 해시되어 저장되는지 테스트"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!@#"
        )
        
        # 비밀번호가 평문으로 저장되지 않는지 확인
        self.assertNotEqual(user.password, "TestPass123!@#")
        # 비밀번호가 해시되었는지 확인 (pbkdf2_sha256으로 시작)
        self.assertTrue(user.password.startswith("pbkdf2_sha256$"))

    def test_user_registration_with_weak_password(self):
        """약한 비밀번호로 회원가입 시도 테스트"""
        # 숫자만으로 이루어진 비밀번호
        response = self.client.post(reverse("register"), {
            "username": "newuser1",
            "email": "new1@example.com",
            "password1": "12345678",
            "password2": "12345678"
        })
        self.assertEqual(response.status_code, 200)
        # 회원가입 실패 확인
        self.assertFalse(User.objects.filter(username="newuser1").exists())

    def test_user_registration_with_username_similar_password(self):
        """사용자명과 유사한 비밀번호로 회원가입 시도 테스트"""
        response = self.client.post(reverse("register"), {
            "username": "johnsmith",
            "email": "john@example.com",
            "password1": "johnsmith123",
            "password2": "johnsmith123"
        })
        self.assertEqual(response.status_code, 200)
        # 회원가입 실패 확인
        self.assertFalse(User.objects.filter(username="johnsmith").exists())

    def test_email_uniqueness(self):
        """이메일 중복 방지 테스트"""
        # 첫 번째 사용자 생성
        User.objects.create_user(
            username="user1",
            email="test@example.com",
            password="TestPass123!@#"
        )
        
        # 동일한 이메일로 두 번째 사용자 생성 시도
        response = self.client.post(reverse("register"), {
            "username": "user2",
            "email": "test@example.com",
            "password1": "TestPass456!@#",
            "password2": "TestPass456!@#"
        })
        
        # 두 번째 사용자 생성 실패 확인
        self.assertEqual(User.objects.filter(email="test@example.com").count(), 1)

    def test_csrf_token_in_registration(self):
        """회원가입 폼에 CSRF 토큰이 있는지 테스트"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_csrf_token_in_login(self):
        """로그인 폼에 CSRF 토큰이 있는지 테스트"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_successful_user_registration(self):
        """정상적인 회원가입 테스트"""
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "SecurePass123!@#",
            "password2": "SecurePass123!@#"
        })
        
        # 회원가입 성공 후 로그인 페이지로 리다이렉트
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        
        # 비밀번호가 해시되었는지 확인
        user = User.objects.get(username="newuser")
        self.assertNotEqual(user.password, "SecurePass123!@#")

    def test_login_with_correct_credentials(self):
        """올바른 자격증명으로 로그인 테스트"""
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!@#"
        )
        
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "TestPass123!@#"
        })
        
        # 로그인 성공 확인
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_incorrect_password(self):
        """잘못된 비밀번호로 로그인 시도 테스트"""
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!@#"
        )
        
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "WrongPassword"
        })
        
        # 로그인 실패 확인
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

