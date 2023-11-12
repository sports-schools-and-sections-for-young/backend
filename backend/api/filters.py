from django_filters.rest_framework import FilterSet, filters
from sections.models import Section, SportType, Address
import django_filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


class LocationFilter(django_filters.FilterSet):
    latitude = django_filters.NumberFilter(field_name='location',
                                           method='filter_latitude')
    longitude = django_filters.NumberFilter(field_name='location',
                                            method='filter_longitude')
    search_radius = filters.NumberFilter(field_name='location',
                                         method='filter_radius')

    def filter_latitude(self, queryset, name, value):
        if value:
            return queryset.filter(location__y=value)
        return queryset

    def filter_longitude(self, queryset, name, value):
        if value:
            return queryset.filter(location__x=value)
        return queryset

    def filter_radius(self, queryset, name, value):
        lon = self.filter_longitude()
        lat = self.filter_longitude()
        queryset = queryset.annotate(distance=Distance('location',
                                                       (lon, lat)))
        queryset = queryset.filter(distance__lte=D(km=value))
        return queryset

    class Meta:
        model = Address
        fields = ['location']


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
    # address = filters.CharFilter

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group', 'price')


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""
    sport_type = filters.ModelChoiceFilter(
        queryset=SportType.objects.all(),
        field_name='title'
    )

    class Meta:
        model = SportType
        fields = ('sport_type', )
