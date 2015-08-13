from collections import namedtuple

from django.db import models
from django.contrib.auth.models import Group

from core.models.base import BaseModel, BaseTag

ProjectStatus = namedtuple("ProjectStatus", ["name"])
PROJECT_STATUS = (
    ProjectStatus("enable"),
    ProjectStatus("disable"),
    ProjectStatus("protected"),
)


class ProjectTag(BaseTag):
    pass


class Project(BaseModel):
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, unique=True, db_index=True,
    )
    description = models.CharField(
        max_length=140, null=False, blank=False,
        default=None, unique=True, db_index=True,
    )
    group = models.ForeignKey(
        Group, null=False,
    )
    status = models.BigIntegerField(choices=tuple(
        (i, t.name) for i, t in enumerate(PROJECT_STATUS)
    ))
    tag_set = models.ManyToManyField(ProjectTag, blank=True)
