from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework import viewsets
from rest_framework import mixins
from sections.models import (
    SportType,
    Section
)

from .filters import SportTypeFilter, SearchFilter
from .serializers import (
    SportTypeSerializer,
    SectionSerializer
)


class SportTypeViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения всех видов спорта из БД."""
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SportTypeFilter
    http_method_names = ('get', )


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class SearchListViewSet(ListViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = SearchFilter
