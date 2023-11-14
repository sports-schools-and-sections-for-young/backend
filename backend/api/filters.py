from django_filters.rest_framework import FilterSet, filters

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
