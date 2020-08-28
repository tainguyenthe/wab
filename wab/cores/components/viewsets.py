from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):

    def get_serializer_context(self):
        context = super(BaseModelViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
