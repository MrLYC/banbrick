import logging
from multiprocessing import pool, cpu_count

from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jsonschema.validators import Draft4Validator as Validator
from jsonschema.exceptions import ValidationError

from ycyc.base.allowfail import AllowFail
from ycyc.base.contextutils import catch
from ycyc.base.lazyutils import LazyKit

from core import models
from core.models import project as project_models
from core.models import item as item_models
from core.models import trigger as trigger_models
from core import exceptions

from apis.utils import auth as auth_utils

logger = logging.getLogger(__name__)
TasksPool = LazyKit(lambda: pool.ThreadPool(cpu_count()))


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

    def update_item(self, item, value):
        item.value = value
        item.strict_save()

    @AllowFail("ItemCollectorView.check_triggers")
    def check_triggers(self, item):
        item_value = item.value
        logger.debug("check_triggers: %s", item.name)
        triggers = trigger_models.Trigger.objects.filter(
            item=item, status=trigger_models.TRIGGER_STATUS.enable,
        )
        for trigger in triggers:
            trigger.on_item_changed(item_value)

    def insert_item_history(self, item, user):
        models.MonitorItemHistory.objects.create(
            item=item, user=user.username,
            status=item.status, value=item.value,
        )

    def post(self, request):
        logger.info("New request for item collector")
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
            project = project_models.Project.objects.get(
                name=project_name,
                group__in=user.groups.all(),
                status=project_models.PROJECT_STATUS.enable,
            )
        except project_models.Project.DoesNotExist as err:
            return Response({
                "ok": False,
                "detail": "enabled project(%s) not found" % project_name,
            }, status=status.HTTP_404_NOT_FOUND)

        item_name = request.data.get("item")
        try:
            item = item_models.MonitorItem.objects.get(
                name=item_name, project=project,
                status=item_models.ITEM_STATUS.enable,
            )
        except item_models.MonitorItem.DoesNotExist as err:
            return Response({
                "ok": False,
                "detail": "enabled item(%s) not found" % item_name,
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                self.update_item(item, request.data.get("value"))
                self.insert_item_history(item, user)
        except exceptions.ModelFieldError as err:
            return Response({
                "ok": False,
                "detail": "value(%s) of item(%s) save failed" % (
                    request.data.get("value"), item_name,
                ),
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        logger.info("Item[%s] has updated", item_name)
        try:
            return Response({
                "ok": True,
                "detail": {
                    "project": project.id,
                    "item": item.id,
                    "value": item.value,
                },
            }, status=status.HTTP_202_ACCEPTED)
        finally:
            with catch():
                TasksPool.apply_async(self.check_triggers, [item])
