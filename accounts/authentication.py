from typing import Optional, Tuple

from django.core import signing
from rest_framework import authentication, exceptions

from accounts.models import Users


TOKEN_SALT = 'accounts.auth'
TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 7


def issue_token(*, user: Users) -> str:
    payload = {'user_ulid': str(user.id), 'user_id': user.user_id}
    return signing.dumps(payload, salt=TOKEN_SALT)


def verify_token(*, token: str) -> Users:
    try:
        payload = signing.loads(token, salt=TOKEN_SALT, max_age=TOKEN_MAX_AGE_SECONDS)
    except signing.BadSignature as exc:
        raise exceptions.AuthenticationFailed('Invalid token') from exc
    except signing.SignatureExpired as exc:
        raise exceptions.AuthenticationFailed('Token expired') from exc

    user_ulid = payload.get('user_ulid')
    if not user_ulid:
        raise exceptions.AuthenticationFailed('Invalid token payload')

    try:
        return Users.objects.get(id=user_ulid)
    except Users.DoesNotExist as exc:
        raise exceptions.AuthenticationFailed('User not found') from exc


class SignedTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request) -> Optional[Tuple[Users, None]]:
        header = request.headers.get('Authorization')
        if not header:
            return None

        parts = header.split(' ', 1)
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Invalid Authorization header')

        user = verify_token(token=parts[1])
        return (user, None)

