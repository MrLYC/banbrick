from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication, exceptions

from banbrick.utils.time import datetime, datetime_now
from apis.utils.auth import is_token_expired
from apis.models import Token


class ApiAuthView(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data={
            "username": request.data.get("u"),
            "password": request.data.get("p"),
        })
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        Token.objects.filter(
            user=serializer.validated_data['user'],
        ).delete()

        now = datetime_now()
        token = Token.objects.create(
            created=now, user=serializer.validated_data['user'],
        )

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
