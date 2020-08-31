from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    ModelSerializer,
)

User = get_user_model()


class UserMiniSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', ]


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        try:
            exclude_fields = ["user_permissions", "password"]
            for field_name in exclude_fields:
                self.fields.pop(field_name)
        except Exception:
            pass
        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BaseSerializer(DynamicFieldsModelSerializer, ModelSerializer):
    """
        Base serializer
    """
    creator = UserMiniSerializer(read_only=True)
    last_modified_by = UserMiniSerializer(read_only=True)
    time_created = DateTimeField(format="%d-%m-%Y %H:%M")
    time_modified = DateTimeField(format="%d-%m-%Y %H:%M")

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(BaseSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class Base64ImageField(CharField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                data = data.split(';base64,')[1]

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension is not None:
                complete_file_name = "%s.%s" % (file_name, file_extension, )

                _file = ContentFile(decoded_file, name=complete_file_name)
                data = default_storage.save(complete_file_name, _file)
                data = settings.MEDIA_URL + data
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
