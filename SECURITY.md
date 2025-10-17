# 보안 가이드

이 문서는 메모짱 애플리케이션의 보안 기능과 베스트 프랙티스를 설명합니다.

## 1. CSRF (Cross-Site Request Forgery) 보호

### 구현 사항
- ✅ 모든 POST 폼에 `{% csrf_token %}` 태그 포함
- ✅ `CsrfViewMiddleware` 활성화
- ✅ CSRF 쿠키 보안 설정 (프로덕션)
  - `CSRF_COOKIE_SECURE = True` (프로덕션)
  - `CSRF_COOKIE_HTTPONLY = True`
  - `CSRF_COOKIE_SAMESITE = "Strict"`

### 검증
- 템플릿 확인: `templates/users/register.html`, `templates/users/login.html`, `templates/memos/memo_form.html`, `templates/memos/memo_confirm_delete.html`
- 테스트: `apps/memos/tests.py` - `test_csrf_protection_on_*`

## 2. XSS (Cross-Site Scripting) 방어

### 구현 사항
- ✅ Django 템플릿 엔진의 자동 이스케이프 기능 활성화 (기본값)
- ✅ `X-Content-Type-Options: nosniff` 헤더 추가
- ✅ `X-Frame-Options: DENY` 헤더 추가

### 향후 개선 사항
Content Security Policy (CSP)를 더 강화하려면 `django-csp` 패키지 사용을 고려하세요:
```bash
pip install django-csp
```

### 검증
- 템플릿 확인: `templates/base.html` - 보안 메타 태그
- 테스트: `apps/memos/tests.py` - `test_xss_protection_in_memo_content`

## 3. SQL Injection 방어

### 구현 사항
- ✅ Django ORM 사용 (파라미터화된 쿼리 자동 생성)
- ✅ Raw SQL 쿼리 사용 안 함
- ✅ 사용자 입력을 직접 SQL에 삽입하지 않음

### 검증
- 코드 확인: `apps/memos/views.py`, `apps/users/views.py`
- 테스트: `apps/memos/tests.py` - `test_sql_injection_protection`

## 4. 비밀번호 보안

### 구현 사항
- ✅ Django의 PASSWORD_VALIDATORS 활성화
  - `UserAttributeSimilarityValidator`: 사용자 정보와 유사한 비밀번호 차단
  - `MinimumLengthValidator`: 최소 8자 이상 요구 (`min_length=8`)
  - `CommonPasswordValidator`: 일반적인 비밀번호 차단
  - `NumericPasswordValidator`: 숫자로만 구성된 비밀번호 차단
- ✅ PBKDF2 SHA256 해시 알고리즘 사용 (Django 기본값)

### 검증
- 설정 확인: `memojjang/settings.py` - `AUTH_PASSWORD_VALIDATORS`
- 테스트: 
  - `apps/memos/tests.py` - `test_password_validation_*`
  - `apps/users/tests.py` - `test_password_hashing`, `test_user_registration_with_weak_password`

## 5. 환경 변수 보안

### 구현 사항
- ✅ `.env` 파일을 `.gitignore`에 추가
- ✅ SECRET_KEY를 환경 변수로 관리
- ✅ 민감 정보 하드코딩 제거
- ✅ `.env.example` 제공 (실제 값은 포함하지 않음)

### SECRET_KEY 생성 방법
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 검증
- 파일 확인:
  - `.gitignore` - `.env` 포함
  - `.env.example` - 템플릿 제공
  - `memojjang/settings.py` - 환경 변수 사용

## 6. 추가 보안 설정

### HTTPS 및 보안 헤더 (프로덕션)
- ✅ `SECURE_SSL_REDIRECT = True` (프로덕션)
- ✅ `SECURE_HSTS_SECONDS = 31536000` (1년, 프로덕션)
- ✅ `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` (프로덕션)
- ✅ `SECURE_HSTS_PRELOAD = True` (프로덕션)
- ✅ `SECURE_CONTENT_TYPE_NOSNIFF = True`
- ✅ `SECURE_BROWSER_XSS_FILTER = True`
- ✅ `X_FRAME_OPTIONS = "DENY"`

### 세션 보안 (프로덕션)
- ✅ `SESSION_COOKIE_SECURE = True` (프로덕션)
- ✅ `SESSION_COOKIE_HTTPONLY = True`
- ✅ `SESSION_COOKIE_SAMESITE = "Strict"`
- ✅ `SESSION_COOKIE_AGE = 86400` (24시간)

### 검증
- 설정 확인: `memojjang/settings.py` - Security settings 섹션
- 테스트: `apps/memos/tests.py` - `test_session_security_after_logout`

## 7. 인증 및 권한

### 구현 사항
- ✅ 로그인 필수 데코레이터 (`@login_required`)
- ✅ 사용자별 데이터 접근 제어
- ✅ 본인의 메모만 조회/수정/삭제 가능

### 검증
- 코드 확인: `apps/memos/views.py` - 모든 뷰에 `@login_required` 적용
- 테스트: 
  - `apps/memos/tests.py` - `test_unauthorized_access_to_memo`, `test_login_required_for_memo_operations`

## 8. 테스트

### 보안 테스트 실행
```bash
# 모든 보안 테스트 실행
python manage.py test

# 특정 보안 테스트만 실행
python manage.py test apps.memos.tests.SecurityTestCase
python manage.py test apps.users.tests.UserSecurityTestCase
```

### Django 보안 체크
```bash
# 기본 체크
python manage.py check

# 배포용 보안 체크
python manage.py check --deploy
```

## 9. 프로덕션 배포 체크리스트

배포 전 다음 사항을 확인하세요:

- [ ] `.env` 파일에서 `DEBUG=False` 설정
- [ ] 강력한 `SECRET_KEY` 생성 및 설정
- [ ] `ALLOWED_HOSTS`에 실제 도메인 추가
- [ ] HTTPS 설정 (인증서 설치)
- [ ] 데이터베이스를 SQLite에서 PostgreSQL/MySQL로 변경 (권장)
- [ ] 정적 파일 수집 (`python manage.py collectstatic`)
- [ ] 환경 변수 백업 및 안전한 저장
- [ ] `python manage.py check --deploy` 실행 및 경고 해결
- [ ] 보안 테스트 실행 (`python manage.py test`)

## 10. OWASP Top 10 (2021) 대응

| OWASP Top 10 | 대응 방안 | 상태 |
|-------------|----------|-----|
| A01:2021 – Broken Access Control | @login_required, 사용자별 데이터 접근 제어 | ✅ |
| A02:2021 – Cryptographic Failures | HTTPS, 쿠키 보안 설정, 비밀번호 해싱 | ✅ |
| A03:2021 – Injection | Django ORM 사용, 파라미터화된 쿼리 | ✅ |
| A04:2021 – Insecure Design | 보안 설계 검토, 테스트 작성 | ✅ |
| A05:2021 – Security Misconfiguration | 보안 설정 강화, DEBUG=False in production | ✅ |
| A06:2021 – Vulnerable Components | 정기적인 패키지 업데이트 | ⚠️ |
| A07:2021 – Identification & Authentication | 강력한 비밀번호 검증, 세션 관리 | ✅ |
| A08:2021 – Software & Data Integrity | 환경 변수 관리, 코드 검증 | ✅ |
| A09:2021 – Security Logging & Monitoring | Django 기본 로깅 | ⚠️ |
| A10:2021 – Server-Side Request Forgery | 현재 해당 없음 (외부 요청 없음) | N/A |

⚠️ = 추가 개선 권장

## 11. 추가 권장 사항

### 의존성 관리
```bash
# 취약점 스캔
pip install safety
safety check

# 패키지 업데이트
pip list --outdated
pip install --upgrade <package>
```

### 로깅 및 모니터링
- 로그인 실패 시도 모니터링
- 비정상적인 활동 감지
- 에러 로그 수집

### 백업
- 정기적인 데이터베이스 백업
- 환경 변수 백업
- 코드 버전 관리 (Git)

### 보안 헤더 추가 (선택 사항)
`django-security` 또는 `django-csp` 패키지 사용 고려:
```bash
pip install django-csp
```

## 참고 자료

- [Django Security Overview](https://docs.djangoproject.com/en/5.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
