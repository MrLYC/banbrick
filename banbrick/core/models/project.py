from collections import namedtuple

from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from ycyc.base.typeutils import constants

from core.models.base import BaseModel, BaseTag

ProjectStatus = namedtuple("ProjectStatus", ["name"])
PROJECT_STATUS_ARRAY = (
    ProjectStatus("enable"),
    ProjectStatus("disable"),
    ProjectStatus("protected"),
)
PROJECT_STATUS = constants(**{
    t.name: i for i, t in enumerate(PROJECT_STATUS_ARRAY)
})


class ProjectTag(BaseTag):
    class Meta:
        verbose_name = _('Project tag')
        verbose_name_plural = _('Project tags')


class Project(BaseModel):
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, unique=True, db_index=True,
        verbose_name=_("Name"),
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
            (i, t.name) for i, t in enumerate(PROJECT_STATUS_ARRAY)
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
