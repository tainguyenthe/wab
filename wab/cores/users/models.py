from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Web App Base OpenSource.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
