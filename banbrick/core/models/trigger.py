from collections import namedtuple
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail

from ycyc.base.iterutils import getattrs
from ycyc.base.allowfail import AllowFail
from ycyc.base.typeutils import constants

from banbrick.utils import time as time_utils

from core.models import base
from core.models import User
from core.models import item as item_models
from core.utils import model as model_utils
from core.exceptions import ModelFieldError

logger = logging.getLogger(__name__)

TriggerStatus = namedtuple("TriggerStatus", ["name"])
TRIGGER_STATUS_ARRAY = (
    TriggerStatus("enable"),
    TriggerStatus("disable"),
    TriggerStatus("protected"),
)
TRIGGER_STATUS = constants(**{
    t.name: i for i, t in enumerate(TRIGGER_STATUS_ARRAY)
})


class Trigger(base.BaseModel):
    ALLOW_OPS = {
        "=", "!=", "<", "<=", ">=", ">",
    }

    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, verbose_name=_("Name"),
        validators=[
            base.BASE_VALIDATORS.safety_string,
        ],
    )
    description = models.CharField(
        max_length=140, null=True, blank=True,
        default=None, verbose_name=_("Description"),
    )
    status = models.BigIntegerField(
        choices=tuple(
            (i, t.name) for i, t in enumerate(TRIGGER_STATUS_ARRAY)
        ), default=0, verbose_name=_("Status"),
    )
    item = models.ForeignKey(
        item_models.MonitorItem, null=False, verbose_name=_("Monitor item"),
    )
    operator = models.CharField(
        max_length=5, null=False, blank=False,
        default=None, verbose_name=_("Operator"),
        choices=((i, i) for i in ALLOW_OPS),
    )
    value = model_utils.ref_field(item_models.MonitorItem, "value")
    active = models.BooleanField(
        default=False, verbose_name=_("Active"),
    )
    active_on = models.DateTimeField(
        default=False, null=True, blank=True,
        verbose_name=_("Active on"),
    )
    alert_user_set = models.ManyToManyField(
        User, blank=True,
        verbose_name=_("Alert user"),
    )

    class Meta:
        verbose_name = _('Trigger')
        verbose_name_plural = _('Triggers')
        unique_together = ('item', 'name',)

    @property
    def expression(self):
        return "item[%s].value %s %s" % (
            self.item.name, self.operator, self.value
        )

    def __str__(self):
        return "%s: %s" % (self.name, self.expression)

    @AllowFail("Trigger.check_condition")
    def check_condition(self, item_value):
        item_type = item_models.ITEM_TYPE[self.item.type]
        value = item_type.factory(self.value)

        operator = self.operator
        if operator == "=":
            return item_value == value
        elif operator == "!=":
            return item_value != value
        elif operator == "<":
            return item_value < value
        elif operator == "<=":
            return item_value <= value
        elif operator == ">=":
            return item_value >= value
        elif operator == ">":
            return item_value > value
        raise ModelFieldError("operator %s is not allowed" % operator)

    @AllowFail("Trigger.on_item_changed")
    def on_item_changed(self, item_value):
        old_active = self.active
        result, exception = self.check_condition(item_value)
        if self.active and not result:
            self.active = False
            self.active_on = None
            self.save()
        elif not self.active and result:
            self.active = True
            self.active_on = time_utils.datetime_now()
            self.save()

        if old_active != self.active:
            email = [u.email for u in self.alert_user_set.all()]
            if email:
                send_mail(
                    "BanBrick Alert",
                    _(
                        "Trigger[{name}] has changed\n"
                        "active_on: {active_on}, active: {active}\n"
                        "item: {item}, expression: {expression}\n"
                        "description: \n{description}\n"
                    ).format(
                        name=self.name, status=self.status,
                        active_on=self.active_on.isoformat(),
                        active=self.active, expression=self.expression,
                        item=self.item.name, item_value=self.item.value,
                        description=self.description,
                    ),
                    getattr(settings, "EMAIL_HOST_USER"),
                    email,
                    fail_silently=True,
                )
