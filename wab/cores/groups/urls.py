from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wab.cores.groups.views import GroupViewSet

app_name = "groups"

router = SimpleRouter()
router.register("v1", GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
