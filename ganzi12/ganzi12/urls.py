from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path, include
from rest_framework import permissions
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Ganzi12 API",
        default_version='v1',
        description="SERVER API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    

    path('adminganzi/', admin.site.urls),
    path('member/', include('member.urls')),
    path('mission/', include('missions.urls')),
    path('challenge/', include('challenges.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)