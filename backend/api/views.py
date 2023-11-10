from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from sections.models import SportType

from .filters import SportTypeFilter
from .serializers import SportTypeSerializer


class SportTypeViewSet(ModelViewSet):
    """Вьюсет для отображения всех видов спорта из БД."""
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SportTypeFilter
    http_method_names = ('get', )
