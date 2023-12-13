from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (CustomAuthenticationToken, RegisterAPIView,
                    SearchSectionViewSet, SectionDeleteAPIView,
                    SetionCreateViewSet, SportOrganizationCreateViewSet,
                    SportTypeCreateViewSet, SportTypeViewSet)

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Sport Hub API",
        default_version='v1',
        description="API documentation"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

router = DefaultRouter()

# Эндпойнт для добавления секции
router.register('create_section', SetionCreateViewSet,
                basename='create_section')
# Эндпойнт для добавления спортшколы
router.register('create_sport_organization', SportOrganizationCreateViewSet,
                basename='create_sport_organization')
# Эндпойнт для добавления вида спорта
router.register('create_sport_types', SportTypeCreateViewSet,
                basename='create_sport_types')
# Эндпойнт для поиска секций
router.register('search_sections', SearchSectionViewSet,
                basename='search_sections')
# Эндпойнт для отображения всех видов спорта
router.register('sport_types', SportTypeViewSet, basename='sport_types')

urlpatterns = [
    path('', include(router.urls)),
    # Эндпойнт для авторизации пользователя
    path('login/', CustomAuthenticationToken.as_view()),
    # Эндпойнт для удаления секции
    path('section/<int:id>/delete/',
         SectionDeleteAPIView.as_view(), name='section_delete'),
    # Эндпойнт для регистрации пользователя
    path('register/', RegisterAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
