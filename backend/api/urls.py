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

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
