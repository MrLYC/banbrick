from django.db import models
from django.contrib.auth.models import User, Group


class BaseModel(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    updated_on = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
    )

    def __str__(self):
        return "<{type}: id={id}>".format(
            type=self.__class__.__name__,
            id=self.id,
        )

    class Meta:
        abstract = True


class BaseTag(BaseModel):
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, unique=True, db_index=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "<{type}: id={id}, name={name}>".format(
            type=self.__class__.__name__,
            name=self.name, id=self.id,
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
    tag_set = models.ManyToManyField(ProjectTag, null=True)


class MonitorItemTag(BaseTag):
    pass


class MonitorItem(BaseModel):
    project = models.ForeignKey(Project, null=False)
    name = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, db_index=True,
    )
    type = models.CharField(
        max_length=64, choices=(
            ("integer", "integer"),
            ("float", "float"),
            ("text", "text"),
            ("boolean", "boolean"),
        ),
    )
    key = models.CharField(
        max_length=64, null=False, blank=False,
        default=None, unique=True, db_index=True,
    )
    value = models.CharField(
        max_length=128, default=None,
    )
    enable = models.BooleanField(default=True)
    tag_set = models.ManyToManyField(MonitorItemTag, null=True)


def _fix_monitor_item_value_by_type(sender, instance, **kwargs):
    type_factory = {
        "integer": int,
        "float": float,
        "text": unicode,
        "boolean": bool,
    }
    factory = type_factory.get(instance.type)
    if factory:
        instance.value = str(factory(instance.value))

models.signals.pre_save.connect(
    _fix_monitor_item_value_by_type,
    sender=MonitorItem,
)
