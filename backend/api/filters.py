from django_filters.rest_framework import FilterSet, filters
import math

from sections.models import Section, SportType


class SearchFilter(FilterSet):
    """Фильтр по полям секции."""
    gender = filters.CharFilter(lookup_expr='startswith')
    sport_type = filters.ModelChoiceFilter(
        queryset=SportType.objects.all(),
        field_name='title'
    )
    age_group = filters.NumberFilter()
    age_group__gte = filters.NumberFilter(
        field_name='age_group',
        lookup_expr='gte'
    )
    age_group__lte = filters.NumberFilter(
        field_name='age_group',
        lookup_expr='lte'
    )
    price = filters.NumberFilter()
    price__gte = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    price__lte = filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )
    # address = filters.CharFilter(method='filter_radius')

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group', 'price')


    def filter_radius(self, queryset, name, value):
        queryset = Section.objects.all()
        lat, lon = value.split(',')
        lat = float(lat),
        lon = float(lon)
        queryset = Section.objects.all()
        for item in queryset:
            lat_1, lon_1 = (item.address.location).split(',')
            lat_1 = float(lat_1)
            lon_1 = float(lon_1)
            distance = self.haversine(lat, lon, lat_1, lon_1)
            if distance <= 1:
                return queryset.filter(address_location=item)
            return queryset
        return queryset


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""
    sport_type = filters.ModelChoiceFilter(
        queryset=SportType.objects.all(),
        field_name='title'
    )

    class Meta:
        model = SportType
        fields = ('sport_type', )
