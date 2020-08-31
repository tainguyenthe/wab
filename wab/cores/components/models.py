"""
    Base model
    with ID, creator, editor, create time. modifi time
"""
from uuid import uuid4

from django.db.models import CASCADE, CharField, DateTimeField, ForeignKey, Model, TextField, UUIDField
from django.utils import timezone


class BaseModel(Model):
    """
        Base
    """
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    time_created = DateTimeField(verbose_name="Created on", auto_now_add=True, null=True)
    time_modified = DateTimeField(verbose_name="Last modified on", auto_now=True, null=True)
    creator = ForeignKey(
        "users.User",
        verbose_name="Created by",
        related_name="%(app_label)s_%(class)s_creator",
        null=True,
        blank=True,
        on_delete=CASCADE
    )
    last_modified_by = ForeignKey(
        "users.User",
        verbose_name="Last modified by",
        related_name="%(app_label)s_%(class)s_last_modified",
        null=True,
        blank=True,
        on_delete=CASCADE
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.time_created:
            self.time_created = timezone.now()

        self.time_modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)


class DynaModel(Model):
    """
        Base
    """
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    time_created = DateTimeField(verbose_name="Created on", auto_now_add=True, null=True)
    time_modified = DateTimeField(verbose_name="Last modified on", auto_now=True, null=True)
    creator = ForeignKey(
        "users.User",
        verbose_name="Created by",
        related_name="%(app_label)s_%(class)s_creator",
        null=True,
        blank=True,
        on_delete=CASCADE
    )
    last_modified_by = ForeignKey(
        "users.User",
        verbose_name="Last modified by",
        related_name="%(app_label)s_%(class)s_last_modified",
        null=True,
        blank=True,
        on_delete=CASCADE
    )
    name = CharField(max_length=500, verbose_name="Name of %(class)s", null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.time_created:
            self.time_created = timezone.now()

        self.time_modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return "%(class)s " + self.name
