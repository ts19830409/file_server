from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,  # noqa: E501
                                            TokenRefreshView)

from django.contrib.auth.decorators import login_required
from files.views import FileViewSet
from stats.views import StatsListView
from users.views import RegisterView, UserDetailView, ContactView, login_view, logout_view

from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView


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

    path('files/', login_required(TemplateView.as_view(template_name='files.html')), name='files-page'),
    path('login/', login_view, name='login-page'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register-page'),

    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile-page'),

    path('about/', TemplateView.as_view(template_name='about.html'), name='about-page'),    
    path('', RedirectView.as_view(url='/login/'), name='home'),
    
    path('logout/', logout_view, name='logout-page'),

]

urlpatterns += [
    path('api/contact/', ContactView.as_view(), name='contact'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)