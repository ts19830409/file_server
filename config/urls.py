from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)  # noqa: E501

from files.views import FileViewSet
from stats.views import StatsListView
from users.views import RegisterView, UserDetailView

router = DefaultRouter()
router.register(r"files", FileViewSet)

schema_view = get_schema_view(
    openapi.Info(title="File Server API", default_version="v1"),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # noqa: E501
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/user/", UserDetailView.as_view(), name="user-detail"),
    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",  # noqa: E501
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",  # noqa: E501
    ),
    path("api/stats/", StatsListView.as_view(), name="stats-list"),
    path("swagger/", schema_view.with_ui("swagger"), name="swagger"),
    path("redoc/", schema_view.with_ui("redoc"), name="redoc"),
]
