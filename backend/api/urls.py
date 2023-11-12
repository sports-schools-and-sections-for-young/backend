from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SportTypeViewSet, SearchListViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('sport_types', SportTypeViewSet, basename='sport_types')
router_v1.register('section_search', SearchListViewSet, basename='searcing')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
