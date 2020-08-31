import os
from importlib import import_module

from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

# API URLS
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    # DRF auth token
    # path("auth-token/", obtain_auth_token),
    path("jwt/jwt-token-auth/", obtain_jwt_token),
    path("jwt/jwt-token-refresh/", refresh_jwt_token),
    path("jwt/jwt-token-verify/", verify_jwt_token),

]

urlpatterns += [
    # Django Admin, use {% url 'admin:index' %}
    # path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("accounts/", include("allauth.urls")),
    # Core Applications
    path("applications/", include("wab.cores.applications.urls", namespace="applications")),
    path("groups/", include("wab.cores.groups.urls", namespace="groups")),
    path("permissions/", include("wab.cores.permissions.urls", namespace="permissions")),
    path("users/", include("wab.cores.users.urls", namespace="users")),

]

# Auto scan premium plugins and add urls
PRE_PLUGINS_DIR = str(settings.APPS_DIR / "premiums")
pre_list = []
for item in os.listdir(PRE_PLUGINS_DIR):
    pre_list.append(item)
    if os.path.isdir(os.path.join(PRE_PLUGINS_DIR, item)) and item != '.git':
        plugin_url = F"wab.premiums.{item}.urls"

        try:
            _module = import_module(plugin_url)
            urlpatterns += [path(F"{item}/", include(plugin_url, namespace=F"{item}")), ]
        except ImportError:
            print('Import Error')

# Auto scan plugins and add urls
PLUGINS_DIR = str(settings.APPS_DIR / "plugins")
for item in os.listdir(PLUGINS_DIR):
    if item not in pre_list:
        if os.path.isdir(os.path.join(PLUGINS_DIR, item)) and item != '.git':
            plugin_url = F"wab.plugins.{item}.urls"

            try:
                _module = import_module(plugin_url)
                urlpatterns += [path(F"{item}/", include(plugin_url, namespace=F"{item}")), ]
            except ImportError:
                pass

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
