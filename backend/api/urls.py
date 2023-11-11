from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SearchSectionViewSet, SportTypeViewSet

app_name = 'api'

router = DefaultRouter()

# Эндпойнт для отображения всех видов спорта из БД
router.register('sport_types', SportTypeViewSet, basename='sport_types')
# Эндпойнт для поиска секций
router.register('search_sections', SearchSectionViewSet,
                basename='search_sections')

schema_view = get_schema_view(
    openapi.Info(
        title="Sport Hub API",
        default_version='v1',
        description="API documentation"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

]
