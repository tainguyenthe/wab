from django.contrib.auth.models import Permission
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wab.cores.components.variables import EXCLUDE_APPS
from wab.cores.permissions.serializers import PermissionSerializer


@api_view(['GET'])
def permissions_view(request):
    perms = Permission.objects.exclude(content_type__app_label__in=EXCLUDE_APPS)

    return Response(PermissionSerializer(perms, many=True, context={"request": request}).data)
