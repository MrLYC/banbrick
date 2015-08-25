from collections import namedtuple
import logging
import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ycyc.base.contextutils import catch
from ycyc.base.typeutils import constants

from core.models.base import BaseModel, BaseTag, BASE_VALIDATORS
from core.models.project import Project
from core.exceptions import ModelFieldError
from core.utils import model as model_utils

logger = logging.getLogger(__name__)
ItemType = namedtuple("ItemType", ["name", "factory"])
ItemStatus = namedtuple("ItemStatus", ["name"])

ITEM_TYPE = (
    ItemType(_("integer"), int),
    ItemType(_("float"), float),
    ItemType(_("text"), unicode),
    ItemType(_("boolean"), bool),
    ItemType(_("decimal"), decimal.Decimal),
)
ITEM_STATUS_ARRAY = (
    ItemStatus(_("enable")),
    ItemStatus(_("disable")),
    ItemStatus(_("protected")),
)


class MonitorItemTag(BaseTag):
    class Meta:
        verbose_name = _('Monitor item tag')
        verbose_name_plural = _('Monitor item tags')


class MonitorItem(BaseModel):
    project = models.ForeignKey(
        Project, null=False, verbose_name=_("Project"),
    )
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, db_index=True, verbose_name=_("Name"),
        validators=[
            BASE_VALIDATORS.safety_string,
        ],
    )
    type = models.BigIntegerField(
        choices=tuple(
            (i, t.name) for i, t in enumerate(ITEM_TYPE)
        ), default=0, verbose_name=_("Type"),
    )
    status = models.BigIntegerField(
        choices=tuple(
            (i, t.name) for i, t in enumerate(ITEM_STATUS_ARRAY)
        ), default=0, verbose_name=_("Status"),
    )
    value = models.CharField(
        max_length=128, default=None, null=True, blank=True,
        verbose_name=_("Value"),
    )
    tag_set = models.ManyToManyField(
        MonitorItemTag, blank=True, verbose_name=_("Tags"),
    )

    class Meta:
        verbose_name = _('Monitor item')
        verbose_name_plural = _('Monitor items')
        unique_together = ('project', 'name',)

    def __str__(self):
        return self.name

    def safe_save(self):
        try:
            self.fix_value()
        except ModelFieldError as err:
            logger.warning(
                "convert item value[%s] by type[%s] failed",
                self.value, self.type,
            )
            self.value = None
        self.save()

    def strict_save(self):
        self.fix_value()
        self.save()

    def fix_value(self):
        with catch(reraise=ModelFieldError):
            type = ITEM_TYPE[self.type]
            self.value = type.factory(self.value)


class MonitorItemHistory(BaseModel):
    item = models.ForeignKey(
        MonitorItem, null=False, db_index=True,
        verbose_name=_("Item"),

    )
    user = models.CharField(
        max_length=64, default=None, verbose_name=_("User"),
    )
    value = model_utils.ref_field(MonitorItem, "value")
    status = model_utils.ref_field(MonitorItem, "status")

    class Meta:
        verbose_name = _('Monitor item history')
        verbose_name_plural = _('Monitor item histories')
