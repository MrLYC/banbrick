from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
import logging

from rest_framework.authentication import TokenAuthentication, exceptions

from banbrick.utils.time import datetime, datetime_now
from apis.utils.auth import is_token_expired
from apis.models import Token

logger = logging.getLogger(__name__)


class ApiAuthView(ObtainAuthToken):
    def post(self, request):
        logger.info("User[%s] require authentication", request.data.get("u"))
        serializer = self.serializer_class(data={
            "username": request.data.get("u"),
            "password": request.data.get("p"),
        })
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime_now()
        with transaction.atomic():
            Token.objects.filter(
                user=serializer.validated_data['user'],
            ).delete()
            token = Token.objects.create(
                created=now, user=serializer.validated_data['user'],
            )
        logger.info("User[%s] authenticate successed", token.user)

        return Response({'token': token.key})

    def delete(self, request):
        auth_key = request.data.get("auth", "")
        authenticate = TokenAuthentication()
        try:
            user, token = authenticate.authenticate_credentials(auth_key)
        except exceptions.AuthenticationFailed as err:
            return Response({
                "ok": False,
                "detail": err.detail,
            }, status=status.HTTP_403_FORBIDDEN)

        token.delete()
        return Response({
            "ok": True,
            "detail": token.created,
        }, status=status.HTTP_202_ACCEPTED)

api_auth_view = ApiAuthView.as_view()
