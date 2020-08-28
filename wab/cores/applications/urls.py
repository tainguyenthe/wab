from django.urls import path, include

from wab.cores.applications.views import applications_view, fields_view

app_name = "applications"

v1patterns = [
    path("", applications_view, name="application_list"),
    path("fields/<str:app_label>/<str:model>/", fields_view, name="field_list"),
]

urlpatterns = [
    path("v1/", include(v1patterns))
]
