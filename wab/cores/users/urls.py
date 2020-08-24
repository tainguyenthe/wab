from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wab.cores.users.api.views import UserViewSet
from wab.cores.users.views import user_detail_view, user_redirect_view, user_update_view

app_name = "users"

router = SimpleRouter()
router.register("v1", UserViewSet)

urlpatterns = [
    # path('api/', include(router.urls)),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),

]
