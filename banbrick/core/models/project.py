from collections import namedtuple

from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from ycyc.base.typeutils import enums

from core.models.base import BaseModel, BaseTag, BASE_VALIDATORS

PROJECT_STATUS = enums("enable", "disable", "protected")


class ProjectTag(BaseTag):
    class Meta:
        verbose_name = _('Project tag')
        verbose_name_plural = _('Project tags')


class Project(BaseModel):
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, unique=True, db_index=True,
        verbose_name=_("Name"), validators=[
            BASE_VALIDATORS.safety_string,
        ],
    )
    description = models.CharField(
        max_length=140, null=True, blank=True,
        default=None, verbose_name=_("Description"),
    )
    group = models.ForeignKey(
        Group, null=False, verbose_name=_("Group"),
    )
    status = models.BigIntegerField(
        choices=tuple(
            (i, _(k)) for k, i in PROJECT_STATUS
        ), default=0, verbose_name=_("Status"),
    )
    tag_set = models.ManyToManyField(
        ProjectTag, blank=True, verbose_name=_("Tags"),
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name
