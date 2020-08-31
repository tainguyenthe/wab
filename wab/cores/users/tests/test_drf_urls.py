import pytest
from django.urls import resolve, reverse

from wab.cores.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("users:user-detail", kwargs={"pk": user.id})
        == f"/users/v1/{user.id}/"
    )
    assert resolve(f"/users/v1/{user.id}/").view_name == "users:user-detail"


def test_user_list():
    assert reverse("users:user-list") == "/users/v1/"
    assert resolve("/users/v1/").view_name == "users:user-list"


def test_user_me():
    assert reverse("users:user-me") == "/users/v1/me/"
    assert resolve("/users/v1/me/").view_name == "users:user-me"
