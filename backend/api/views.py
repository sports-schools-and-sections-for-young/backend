from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework import viewsets
from rest_framework import mixins
# generics
from sections.models import (
    SportType,
    # Shedule,
    # AgeGroup,
    Section
)
from organizations.models import (
    Rewiev
#     Address,
#     SportOrganization,
)

from .filters import SportTypeFilter, SearchFilter, LocationFilter
from .serializers import (
    SportTypeSerializer,
    SectionSerializer,
    # SheduleSerializer,
    RewievSerializer,
    # AgeGroupSerializer,
    # AddressSerializer,
    # SportOrganizationSerializer,
    # CoordinatSerializer
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
    ilter_class = SearchFilter

    def get_queryset(self):
        queryset = Section.objects.all()
        section_filter = SearchFilter(self.request.GET, queryset=queryset)
        queryset = section_filter.qs
        location_filter = LocationFilter(self.request.GET, queryset=queryset)
        queryset = location_filter
        return queryset
