from django_filters.rest_framework import FilterSet, filters
from sections.models import Section, SportType


class SearchSectionFilter(FilterSet):
    """
    Фильтр для поиска секций по следующим полям: пол ребенка, вид спорта,
    возраст ребенка, стоимость занятий, адрес.
    """
    age_group = filters.NumberFilter(method='get_age_group')
    price = filters.NumberFilter(method='get_price')
    address = filters.CharFilter(method='get_address')

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group', 'price', 'address')

    def get_age_group(self, queryset, name, value):
        return queryset.filter(
            age_group__year_until__gte=value, age_group__year_from__lte=value)

    def get_price(self, queryset, name, value):
        return queryset.filter(price__gte=0, price__lte=value)

    def get_address(self, queryset, name, value):
        return queryset.filter(address__full_address__icontains=value)


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""

    class Meta:
        model = SportType
        fields = ('title', )
