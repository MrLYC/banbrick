from collections import namedtuple

from django.db import models

from ycyc.base.contextutils import catch

from core.models.base import BaseModel, BaseTag
from core.models.project import Project
from core.exceptions import ModelFieldValdateError

ItemType = namedtuple("ItemType", ["name", "factory"])
ItemStatus = namedtuple("ItemStatus", ["name"])

ITEM_TYPE = (
    ItemType("integer", int),
    ItemType("float", float),
    ItemType("text", unicode),
    ItemType("boolean", bool),
)
ITEM_STATUS = (
    ItemStatus("enable"),
    ItemStatus("disable"),
    ItemStatus("protected"),
)


class MonitorItemTag(BaseTag):
    pass


class MonitorItem(BaseModel):
    project = models.ForeignKey(Project, null=False)
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, db_index=True,
    )
    type = models.BigIntegerField(choices=tuple(
        (i, t.name) for i, t in enumerate(ITEM_TYPE)
    ))
    status = models.BigIntegerField(choices=tuple(
        (i, t.name) for i, t in enumerate(ITEM_STATUS)
    ))
    key = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, unique=True, db_index=True,
    )
    value = models.CharField(
        max_length=128, default=None,
    )
    enable = models.BooleanField(default=True)
    tag_set = models.ManyToManyField(MonitorItemTag, blank=True)


def _fix_monitor_item_value_by_type(sender, instance, **kwargs):
    with catch(reraise=ModelFieldValdateError):
        type = ITEM_TYPE[instance.type]
        instance.value = type.factory(instance.value)

models.signals.pre_save.connect(
    _fix_monitor_item_value_by_type,
    sender=MonitorItem,
)
