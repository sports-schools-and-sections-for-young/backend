from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (CustomAuthenticationToken, DeleteUserAPIView,
                    ProfileAPIView, RegisterAPIView, ResetPasswordAPIView,
                    SearchSectionViewSet, SectionAPIView, SectionCreateViewSet,
                    SectionDeleteAPIView, SectionUpdateViewSet,
                    SportOrganizationCreateViewSet,
                    SportOrganizationUpdateViewSet, SportTypeAllViewSet,
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
router.register('create_section', SectionCreateViewSet,
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
router.register('sport_types_all', SportTypeAllViewSet,
                basename='sport_types_all')
# Эндпойнт для отображения видов спорта, которые привязаны хотя бы к одной
# секции
router.register('sport_types', SportTypeViewSet, basename='sport_types')

urlpatterns = [
    path('', include(router.urls)),
    # Эндпойнт для авторизации пользователя
    path('login/', CustomAuthenticationToken.as_view()),
    # Эндпойнт для регистрации пользователя
    path('register/', RegisterAPIView.as_view()),
    # Эндпойнт для смены пароля пользователя
    path('reset_password/', ResetPasswordAPIView.as_view()),
    # Эндпойнт для удаления пользователя
    path('user/delete/', DeleteUserAPIView.as_view()),
    # Эндпойнт для удаления секции
    path('section/<int:id>/delete/',
         SectionDeleteAPIView.as_view(), name='section_delete'),
    # Эндпойнт для просмотра спортшколы в личном кабинете
    path('sport_school/',
         ProfileAPIView.as_view(), name='section_delete'),
    # Эндпойнт для редактирования спортшколы
    path('sport_school/update/',
         SportOrganizationUpdateViewSet.as_view({'patch': 'partial_update'})),
    # Эндпойнт для просмотра всех секции пользователя в профиле
    path('section/', SectionAPIView.as_view(), name='section'),
    # Эндпойнт для редактирования секции
    path('section/<int:pk>/update/', SectionUpdateViewSet.as_view(
        {'patch': 'partial_update'})),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
