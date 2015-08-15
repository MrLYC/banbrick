from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions

from core import models as core_models

EXPIRE_SECONDS = timedelta(
    seconds=getattr(settings, 'REST_API_AUTH_EXPIRES', 60),
)


def is_token_expired(token, now=None):
    now = timezone.now() if now is None else now
    return token.created < now - EXPIRE_SECONDS


def authenticate_from_key(auth_key):
    authenticate = TokenAuthentication()
    user, token = authenticate.authenticate_credentials(auth_key)
    if is_token_expired(token):
        token.delete()
        raise exceptions.AuthenticationFailed("token is expired")
    return user


def is_user_own_project(user, project):
    try:
        user.groups.get(id=project.group_id)
        return True
    except core_models.Group.DoesNotExist as err:
        return False
