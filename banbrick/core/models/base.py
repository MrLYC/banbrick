from django.db import models


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
