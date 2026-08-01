from dataclasses import dataclass

from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Authentication, LoginCredential, Users


PASSWORD_AUTH_PATH = '/oauth/password/callback'


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
            f'Authentication row not found for auth_path={PASSWORD_AUTH_PATH}'
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
        raise RegistrationError('User creation failed due to duplicate data') from exc


def login_user(*, login: str, password: str) -> AuthResult:
    cred = (
        LoginCredential.objects.select_related('user_ulid')
        .filter(enable_flag=True)
        .filter(username=login)
        .first()
    )
    if cred is None:
        cred = (
            LoginCredential.objects.select_related('user_ulid')
            .filter(enable_flag=True)
            .filter(email=login)
            .first()
        )

    if cred is None:
        raise LoginError('Invalid credentials')

    if not check_password(password, cred.password_hash):
        raise LoginError('Invalid credentials')

    return AuthResult(user=cred.user_ulid)

