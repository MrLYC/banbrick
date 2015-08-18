from collections import namedtuple
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ycyc.base.iterutils import getattrs
from ycyc.base.allowfail import AllowFail
from ycyc.base.typeutils import constants

from banbrick.utils import time as time_utils

from core.models import base
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


class Context(object):
    ALLOW_VARS = {
        "item.name", "item.type", "item.status", "item.value",
        "trigger.name", "trigger.status", "trigger.active",
    }

    def __init__(self, item, trigger):
        self.item = item
        self.trigger = trigger

    def variables(self, name):
        if name not in self.ALLOW_VARS:
            return None
        return getattrs(self, name.split("."))


class Trigger(base.BaseModel):
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
    active = models.BooleanField(
        default=False, verbose_name=_("Active"),
    )
    active_on = models.DateTimeField(
        default=False, null=True, blank=True,
        verbose_name=_("Active on"),
    )

    class Meta:
        verbose_name = _('Trigger')
        verbose_name_plural = _('Triggers')
        unique_together = ('item', 'name',)

    def __str__(self):
        return self.name

    @AllowFail("Trigger.check_conditions")
    def check_conditions(self, item):
        context = Context(item, self)
        conditions = list(Condition.objects.filter(trigger=self))
        if conditions:
            for cond in conditions:
                result, exception = cond.check_context(context)
                if exception or not result:
                    break
            else:
                return True

        return False

    @AllowFail("Trigger.on_item_changed")
    def on_item_changed(self, item):
        result, exception = self.check_conditions(item)
        if self.active and not result:
            self.active = False
            self.active_on = None
            self.save()
        elif not self.active and result:
            self.active = True
            self.active_on = time_utils.datetime_now()
            self.save()


class Condition(base.BaseModel):
    ALLOW_OPS = {
        "=", "!=", "<", "<=", ">=", ">",
    }

    trigger = models.ForeignKey(
        Trigger, null=False, verbose_name=_("Trigger"),
    )
    variable = models.CharField(
        max_length=32, null=False, blank=False,
        default=None, verbose_name=_("Variable"),
        choices=((i, i) for i in Context.ALLOW_VARS),
    )
    operator = models.CharField(
        max_length=5, null=False, blank=False,
        default=None, verbose_name=_("Operator"),
        choices=((i, i) for i in ALLOW_OPS),
    )
    type = model_utils.ref_field(item_models.MonitorItem, "type")
    value = model_utils.ref_field(item_models.MonitorItem, "value")

    class Meta:
        verbose_name = _('Trigger condition')
        verbose_name_plural = _('Trigger conditions')

    @AllowFail("Condition.check_context")
    def check_context(self, context):
        item_type = item_models.ITEM_TYPE[self.type]
        value = item_type.factory(self.value)
        var_value = context.variables(self.variable)

        operator = self.operator
        if operator == "=":
            return var_value == value
        elif operator == "!=":
            return var_value != value
        elif operator == "<":
            return var_value < value
        elif operator == "<=":
            return var_value <= value
        elif operator == ">=":
            return var_value >= value
        elif operator == ">":
            return var_value > value
        raise ModelFieldError("operator %s is not allowed" % operator)

    def __str__(self):
        return "{%s} %s %s" % (self.variable, self.operator, self.value)
