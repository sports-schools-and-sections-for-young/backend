from django.db.models import Q  # Для работы с несколькими условиями
from django_filters.rest_framework import FilterSet, filters
from sections.models import Section, SportType


class SearchSectionFilter(FilterSet):
    """Фильтр по полям секции."""

    sport_type = filters.ModelChoiceFilter(
        queryset=SportType.objects.all(),
        field_name='title'
    )
    age_group = filters.NumberFilter(method='get_age_group')
    price = filters.NumberFilter(method='get_price')
    address = filters.CharFilter(method='get_address')

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group', 'price', 'address')

    def get_age_group(self, queryset, name, value):
        return queryset.filter(
            age_group__year_from__lte=value, age_group__year_until__gte=value)

    def get_price(self, queryset, name, value):
        return queryset.filter(price__gte=value)

    def get_address(self, queryset, name, value):
        return queryset.filter(
            Q(address__index__icontains=value)
            | Q(address__city__icontains=value)
            | Q(address__metro__icontains=value)
            | Q(address__district__icontains=value)
            | Q(address__street__icontains=value)
            | Q(address__house__icontains=value)
        )


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""
    sport_type = filters.ModelChoiceFilter(
        queryset=SportType.objects.all(),
        field_name='title'
    )

    class Meta:
        model = SportType
        fields = ('sport_type', )
