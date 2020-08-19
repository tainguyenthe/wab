import pytest
from django.urls import resolve, reverse

from wab.cores.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("users:user-detail", kwargs={"username": user.username})
        == f"/users/api/v1/{user.username}/"
    )
    assert resolve(f"/users/api/v1/{user.username}/").view_name == "users:user-detail"


def test_user_list():
    assert reverse("users:user-list") == "/users/api/v1/"
    assert resolve("/users/api/v1/").view_name == "users:user-list"


def test_user_me():
    assert reverse("users:user-me") == "/users/api/v1/me/"
    assert resolve("/users/api/v1/me/").view_name == "users:user-me"
