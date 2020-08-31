from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from wab.cores.components.serializers import DynamicFieldsModelSerializer

User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserMiniSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', ]
