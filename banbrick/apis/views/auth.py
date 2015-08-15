from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apis.utils.time import datetime, datetime_now
from apis.utils.auth import is_token_expired


class ApiAuthView(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(
            user=serializer.validated_data['user'],
        )
        now = datetime_now()

        if is_token_expired(token, now):
            token.created = now
            token.save()

        return Response({'token': token.key})


api_auth_view = ApiAuthView.as_view()
