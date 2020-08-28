from django.urls import path

from wab.cores.applications.views import applications_view, fields_view

app_name = "applications"
urlpatterns = [
    path("applications/", applications_view, name="application_list"),
    path("fields/<str:app_label>/<str:model>/", fields_view, name="field_list"),
]
