from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from apis.utils.time import datetime, datetime_now
from apis.utils.auth import is_token_expired
from apis.models import Token


class ApiAuthView(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = datetime_now()
        tokens = list(Token.objects.filter(
            user=serializer.validated_data['user'],
        ).order_by('created'))
        for token in tokens:
            if is_token_expired(token, now):
                token.delete()
            else:
                break
        else:
            token = Token.objects.create(
                created=now, user=serializer.validated_data['user'],
            )

        return Response({'token': token.key})

api_auth_view = ApiAuthView.as_view()
