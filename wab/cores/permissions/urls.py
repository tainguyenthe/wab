from django.urls import include, path

from wab.cores.permissions.views import permissions_view

app_name = "permissions"

v1patterns = [
    path("", permissions_view, name="permission_list"),
]

urlpatterns = [
    path("v1/", include(v1patterns)),
]
