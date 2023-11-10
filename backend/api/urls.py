from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SportTypeViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('sport_types', SportTypeViewSet, basename='sport_types')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
