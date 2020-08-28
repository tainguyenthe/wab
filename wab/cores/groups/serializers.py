from django.contrib.auth.models import Group

from wab.cores.components.serializers import DynamicFieldsModelSerializer


class GroupSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"
