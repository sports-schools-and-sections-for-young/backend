from django_filters.rest_framework import FilterSet, filters
from sections.models import DayOfWeek, Section, SportType


class SearchSectionFilter(FilterSet):
    """
    Фильтр для поиска секций по следующим полям: пол ребенка, вид спорта,
    возраст ребенка, стоимость занятий, адрес секции, день недели работы
    секции.
    """
    age_group = filters.NumberFilter(method='get_age_group')
    sport_type = filters.ModelMultipleChoiceFilter(
        label='Вид спорта',
        queryset=SportType.objects.all(),
        field_name='sport_type__title',
        to_field_name='title'
    )
    price = filters.NumberFilter(method='get_price')
    address = filters.CharFilter(method='get_address')
    day_of_week = filters.ModelMultipleChoiceFilter(
        label='День недели',
        queryset=DayOfWeek.objects.all(),
        field_name='schedule__day__title',
        to_field_name='title'
    )

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group',
                  'price', 'address', 'day_of_week', 'free_class')

    # Фильтр по возрасту ребенка
    def get_age_group(self, queryset, name, value):
        return queryset.filter(
            age_group__year_until__gte=value, age_group__year_from__lte=value)

    # Фильтр по стоимости занятий
    def get_price(self, queryset, name, value):
        return queryset.filter(price__gte=0, price__lte=value)

    # Фильтр по адресу секции
    def get_address(self, queryset, name, value):
        for item in value.split():
            queryset = queryset.filter(
                address__full_address__icontains=item)
        return queryset


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""

    class Meta:
        model = SportType
        fields = ('title', )
