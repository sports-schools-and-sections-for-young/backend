from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework import viewsets
from rest_framework import mixins
from sections.models import (
    SportType,
    Section
)

from .filters import SportTypeFilter, SearchSectionFilter
from .serializers import (
    SportTypeSerializer,
    SectionSerializer
)


class SportTypeViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения всех видов спорта."""
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SportTypeFilter
    http_method_names = ('get', )


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class SearchListViewSet(ListViewSet):
    """Вьюсет для отображения секций в поиске."""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = SearchSectionFilter
