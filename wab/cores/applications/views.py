from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wab.cores.components.variables import (
    EXCLUDE_APPS,
    PROTECTED_APPS,
    PROTECTED_FIELDS,
)


@api_view(['GET'])
def applications_view(request):
    _apps = ContentType.objects.exclude(app_label__in=PROTECTED_APPS)

    return Response([
        {
            "app_label": app.app_label,
            "model": app.model,
            "app_verbose_name": apps.get_app_config(app.app_label).verbose_name,
            "model_verbose_name": apps.get_model(app.app_label, app.model)._meta.verbose_name.title(),
        } for app in _apps
    ])


@api_view(['GET'])
def fields_view(request, app_label, model):
    try:
        _model = apps.get_model(app_label, model)
        fields = _model._meta.concrete_fields
        return Response(
            [
                {
                    'name': _field.name,
                    'verbose_name': _field.verbose_name,
                    'type': _field.__class__.__name__
                } for _field in fields if not _field.name in PROTECTED_FIELDS
            ]
        )
    except Exception:
        return Response({})
