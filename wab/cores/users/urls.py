from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wab.cores.users.views import UserViewSet

app_name = "users"

router = SimpleRouter()
router.register("v1", UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
