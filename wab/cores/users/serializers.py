from django.contrib.auth import get_user_model

from wab.cores.components.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
