from django.contrib.auth.models import Permission

from wab.cores.components.serializers import DynamicFieldsModelSerializer


class PermissionSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Permission
        fields = "__all__"
