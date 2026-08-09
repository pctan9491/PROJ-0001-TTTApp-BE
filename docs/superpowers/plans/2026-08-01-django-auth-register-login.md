# Django Auth (Register/Login) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a new Django backend connected to an existing PostgreSQL DB and implement password-based registration + login REST APIs backed by `Users`, `Login_Credential`, and `Authentication`.

**Architecture:** Django REST Framework endpoints call a small accounts service layer that performs DB reads/writes through Django models mapped to existing tables. Passwords are hashed with Django hashers. Tokens are issued/verified using Django signing (opaque bearer token).

**Tech Stack:** Python, Django, Django REST Framework, PostgreSQL, psycopg2-binary

---

## Target Folder

Run everything inside:

- `c:\Users\User\Documents\Project\PROJ-0001 To-do targetting app\To-Do targetting app BE`

## Environment Variables

Use a `.env` file in project root (do not commit secrets). Example values:

```dotenv
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

## File/Module Map (End State)

**Created by Django startproject**

- `manage.py`
- `config/settings.py`
- `config/urls.py`
- `config/asgi.py`
- `config/wsgi.py`

**Created by this plan**

- `requirements.txt`
- `.env.example`
- `accounts/apps.py`
- `accounts/models.py`
- `accounts/serializers.py`
- `accounts/services.py`
- `accounts/authentication.py`
- `accounts/views.py`
- `accounts/urls.py`

---

### Task 1: Bootstrap Django + Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`

- [ ] **Step 1: Create virtual environment**

Run (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Expected: pip upgrades successfully.

- [ ] **Step 2: Install dependencies**

Run:

```powershell
pip install Django djangorestframework psycopg2-binary python-dotenv
```

Expected: packages install without errors.

- [ ] **Step 3: Freeze dependencies**

Run:

```powershell
pip freeze > requirements.txt
```

Expected: `requirements.txt` contains Django, djangorestframework, psycopg2-binary, python-dotenv.

- [ ] **Step 4: Add `.env.example`**

Create file `.env.example` with:

```dotenv
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .env.example
git commit -m "chore: bootstrap django dependencies"
```

---

### Task 2: Create Django Project + Accounts App

**Files:**
- Create: `manage.py`
- Create: `config/*`
- Create: `accounts/*`

- [ ] **Step 1: Start Django project in current folder**

Run:

```powershell
django-admin startproject config .
```

Expected: `manage.py` and `config/` are created.

- [ ] **Step 2: Create accounts app**

Run:

```powershell
python manage.py startapp accounts
```

Expected: `accounts/` folder exists with default Django app files.

- [ ] **Step 3: Commit**

```bash
git add manage.py config accounts
git commit -m "chore: init django project and accounts app"
```

---

### Task 3: Configure Settings (PostgreSQL + DRF + Env)

**Files:**
- Modify: `config/settings.py`
- Modify: `config/urls.py`

- [ ] **Step 1: Update `config/settings.py`**

Replace/ensure the following pieces exist (adjust only where needed).

```python
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.authentication.SignedTokenAuthentication",
    ],
}
```

- [ ] **Step 2: Update `config/urls.py`**

Ensure:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
]
```

- [ ] **Step 3: Run a basic system check**

Run:

```powershell
python manage.py check
```

Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 4: Commit**

```bash
git add config/settings.py config/urls.py
git commit -m "chore: configure postgres env and drf"
```

---

### Task 4: Map Existing Tables with Django Models

**Files:**
- Modify: `accounts/models.py`

- [ ] **Step 1: Implement models**

Set `managed = False` so Django does not manage your existing tables.

```python
import uuid

from django.db import models


class Authentication(models.Model):
    id = models.UUIDField(primary_key=True)
    auth_path = models.CharField(max_length=30)

    class Meta:
        db_table = "Authentication"
        managed = False


class Users(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    gender = models.CharField(max_length=2)
    birth_date = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "Users"
        managed = False


class LoginCredential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_ulid = models.ForeignKey(
        Users,
        db_column="user_ulid",
        to_field="id",
        on_delete=models.CASCADE,
        related_name="login_credentials",
    )
    user_id = models.CharField(max_length=10, db_column="user_id")
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    auth_ulid = models.ForeignKey(
        Authentication,
        db_column="auth_ulid",
        to_field="id",
        on_delete=models.CASCADE,
        related_name="login_credentials",
    )
    enable_flag = models.BooleanField(default=True)
    biometric_info = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "Login_Credential"
        managed = False
```

- [ ] **Step 2: Validate model import**

Run:

```powershell
python manage.py shell -c "from accounts.models import Users, LoginCredential, Authentication; print(Users, LoginCredential, Authentication)"
```

Expected: prints the three model classes without errors.

- [ ] **Step 3: Commit**

```bash
git add accounts/models.py
git commit -m "feat: map existing auth tables"
```

---

### Task 5: Implement Auth Service (Register + Login)

**Files:**
- Create: `accounts/services.py`

- [ ] **Step 1: Create `accounts/services.py`**

```python
from dataclasses import dataclass

from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Authentication, LoginCredential, Users


PASSWORD_AUTH_PATH = "/oauth/password/callback"


@dataclass(frozen=True)
class AuthResult:
    user: Users


class RegistrationError(Exception):
    pass


class LoginError(Exception):
    pass


def _get_password_auth() -> Authentication:
    try:
        return Authentication.objects.get(auth_path=PASSWORD_AUTH_PATH)
    except Authentication.DoesNotExist as exc:
        raise RegistrationError(
            f"Authentication row not found for auth_path={PASSWORD_AUTH_PATH}"
        ) from exc


def register_user(
    *,
    user_id: str,
    first_name: str,
    last_name: str,
    gender: str,
    birth_date,
    username: str,
    email: str,
    password: str,
) -> AuthResult:
    auth = _get_password_auth()

    try:
        with transaction.atomic():
            user = Users.objects.create(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_date=birth_date,
                created_at=timezone.now(),
            )

            LoginCredential.objects.create(
                user_ulid=user,
                user_id=user.user_id,
                username=username,
                email=email,
                password_hash=make_password(password),
                auth_ulid=auth,
                enable_flag=True,
                created_at=timezone.now(),
            )

            return AuthResult(user=user)
    except IntegrityError as exc:
        raise RegistrationError("User creation failed due to duplicate data") from exc


def login_user(*, login: str, password: str) -> AuthResult:
    cred = (
        LoginCredential.objects.select_related("user_ulid")
        .filter(enable_flag=True)
        .filter(username=login)
        .first()
    )
    if cred is None:
        cred = (
            LoginCredential.objects.select_related("user_ulid")
            .filter(enable_flag=True)
            .filter(email=login)
            .first()
        )

    if cred is None:
        raise LoginError("Invalid credentials")

    if not check_password(password, cred.password_hash):
        raise LoginError("Invalid credentials")

    return AuthResult(user=cred.user_ulid)
```

- [ ] **Step 2: Commit**

```bash
git add accounts/services.py
git commit -m "feat: add registration and login services"
```

---

### Task 6: Token Issuing + Authentication (Bearer Token)

**Files:**
- Create: `accounts/authentication.py`

- [ ] **Step 1: Create `accounts/authentication.py`**

This implements DRF authentication using Django’s signing.

```python
from typing import Optional, Tuple

from django.core import signing
from rest_framework import authentication, exceptions

from accounts.models import Users


TOKEN_SALT = "accounts.auth"
TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 7


def issue_token(*, user: Users) -> str:
    payload = {"user_ulid": str(user.id), "user_id": user.user_id}
    return signing.dumps(payload, salt=TOKEN_SALT)


def verify_token(*, token: str) -> Users:
    try:
        payload = signing.loads(token, salt=TOKEN_SALT, max_age=TOKEN_MAX_AGE_SECONDS)
    except signing.BadSignature as exc:
        raise exceptions.AuthenticationFailed("Invalid token") from exc
    except signing.SignatureExpired as exc:
        raise exceptions.AuthenticationFailed("Token expired") from exc

    user_ulid = payload.get("user_ulid")
    if not user_ulid:
        raise exceptions.AuthenticationFailed("Invalid token payload")

    try:
        return Users.objects.get(id=user_ulid)
    except Users.DoesNotExist as exc:
        raise exceptions.AuthenticationFailed("User not found") from exc


class SignedTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request) -> Optional[Tuple[Users, None]]:
        header = request.headers.get("Authorization")
        if not header:
            return None

        parts = header.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid Authorization header")

        user = verify_token(token=parts[1])
        return (user, None)
```

- [ ] **Step 2: Commit**

```bash
git add accounts/authentication.py
git commit -m "feat: add signed token authentication"
```

---

### Task 7: Serializers + Views + URLs

**Files:**
- Create: `accounts/serializers.py`
- Create: `accounts/views.py`
- Create: `accounts/urls.py`

- [ ] **Step 1: Create `accounts/serializers.py`**

```python
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=70)
    last_name = serializers.CharField(max_length=70)
    gender = serializers.CharField(max_length=2)
    birth_date = serializers.DateField()

    username = serializers.CharField(max_length=70)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)
```

- [ ] **Step 2: Create `accounts/views.py`**

```python
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import issue_token
from accounts.serializers import LoginSerializer, RegisterSerializer
from accounts.services import LoginError, RegistrationError, login_user, register_user


def _user_payload(user):
    return {
        "id": str(user.id),
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "birth_date": user.birth_date.isoformat(),
    }


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = register_user(**serializer.validated_data)
        except RegistrationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        token = issue_token(user=result.user)
        return Response(
            {"access_token": token, "user": _user_payload(result.user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = login_user(**serializer.validated_data)
        except LoginError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        token = issue_token(user=result.user)
        return Response({"access_token": token, "user": _user_payload(result.user)})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"user": _user_payload(user)})
```

- [ ] **Step 3: Create `accounts/urls.py`**

```python
from django.urls import path

from accounts.views import LoginView, MeView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
]
```

- [ ] **Step 4: Run Django checks**

Run:

```powershell
python manage.py check
```

Expected: no issues.

- [ ] **Step 5: Commit**

```bash
git add accounts/serializers.py accounts/views.py accounts/urls.py
git commit -m "feat: add auth endpoints register login me"
```

---

### Task 8: Manual Verification with SOAP UI (or curl)

**Files:**
- None

- [ ] **Step 1: Ensure `.env` exists with real DB values**

Create `.env` in project root (same folder as `manage.py`) and fill in real DB connection values.

- [ ] **Step 2: Start server**

Run:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Expected: server starts without errors.

- [ ] **Step 3: Register**

Request:

`POST http://127.0.0.1:8000/api/auth/register/`

Body JSON:

```json
{
  "user_id": "U000000001",
  "first_name": "Test",
  "last_name": "User",
  "gender": "M",
  "birth_date": "2000-01-01",
  "username": "testuser1",
  "email": "test1@example.com",
  "password": "Passw0rd1234"
}
```

Expected:
- HTTP 201
- JSON includes `access_token` and `user`

- [ ] **Step 4: Login**

Request:

`POST http://127.0.0.1:8000/api/auth/login/`

Body JSON:

```json
{
  "login": "testuser1",
  "password": "Passw0rd1234"
}
```

Expected:
- HTTP 200
- JSON includes `access_token`

- [ ] **Step 5: Me**

Request:

`GET http://127.0.0.1:8000/api/auth/me/`

Header:
- `Authorization: Bearer <access_token>`

Expected:
- HTTP 200
- JSON includes `user`

- [ ] **Step 6: DB verification in pgAdmin**

Confirm rows exist:
- one in `Users`
- one in `Login_Credential` referencing that user

---

## Plan Self-Review

- Spec coverage: plan implements register/login/me, uses `/oauth/password/callback` Authentication row, hashes passwords, returns bearer token.
- Placeholder scan: no TBD/TODO steps.
- Type consistency: `Users` is used consistently as request.user for authenticated endpoints.

