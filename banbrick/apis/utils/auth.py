from datetime import timedelta

from django.conf import settings
from django.utils import timezone

EXPIRE_SECONDS = timedelta(
    seconds=getattr(settings, 'REST_API_AUTH_EXPIRES', 60),
)


def is_token_expired(token, now=None):
    now = timezone.now() if now is None else now
    return token.created < now - EXPIRE_SECONDS
