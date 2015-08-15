from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jsonschema.validators import Draft4Validator as Validator
from jsonschema.exceptions import ValidationError

from core import models

from apis.utils import auth as auth_utils


class ItemCollectorView(APIView):
    PostValidator = Validator({
        "type": "object",
        "required": ["auth", "project", "item", "value"],
        "properties": {
            "auth": {
                "type": "string",
                "minLength": 1,
            },
            "project": {
                "type": "string",
                "minLength": 1,
            },
            "item": {
                "type": "string",
                "minLength": 1,
            },
            "value": {
                "type": ["string", "null"],
            },
        },
    })

    def post(self, request):
        try:
            self.PostValidator.validate(request.data)
        except ValidationError as err:
            return Response({
                "ok": False,
                "detail": err.message,
            }, status=status.HTTP_400_BAD_REQUEST)

        auth_key = request.data.get("auth")
        try:
            user = auth_utils.authenticate_from_key(auth_key)
        except auth_utils.exceptions.AuthenticationFailed as err:
            return Response({
                "ok": False,
                "detail": err.detail,
            }, status=status.HTTP_401_UNAUTHORIZED)

        project_name = request.data.get("project")
        try:
            project = models.Project.objects.get(name=project_name)
        except models.Project.DoesNotExist as err:
            return Response({
                "ok": False,
                "detail": "project(%s) not found" % project_name,
            }, status=status.HTTP_404_NOT_FOUND)

        if not auth_utils.is_user_own_project(user, project):
            return Response({
                "ok": False,
                "detail": "user(%s) has no permission for project(%s)" % (
                    user.username, project_name,
                ),
            }, status=status.HTTP_403_FORBIDDEN)

        item_name = request.data.get("item")
        try:
            item = models.MonitorItem.objects.get(
                name=item_name, project=project,
            )
        except models.MonitorItem.DoesNotExist as err:
            return Response({
                "ok": False,
                "detail": "item(%s) not found" % item_name,
            }, status=status.HTTP_404_NOT_FOUND)

        item.value = request.data.get("value")
        try:
            item.fix_value()
            item.save()
        except Exception as err:
            return Response({
                "ok": False,
                "detail": "value(%s) of item(%s) save failed" % (
                    request.data.get("value"), item_name,
                ),
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response({
            "ok": True,
            "detail": {
                "project": project.id,
                "item": item.id,
                "value": item.value,
            },
        }, status=status.HTTP_202_ACCEPTED)
