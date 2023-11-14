from django_filters.rest_framework import FilterSet, filters
from sections.models import Section, SportType, DayOfWeek


class SearchSectionFilter(FilterSet):
    """
    Фильтр для поиска секций по следующим полям: пол ребенка, вид спорта,
    возраст ребенка, стоимость занятий, адрес секции.
    """
    age_group = filters.NumberFilter(method='get_age_group')
    sport_type = filters.ModelMultipleChoiceFilter(
        queryset=SportType.objects.all()
    )
    price = filters.NumberFilter(method='get_price')
    address = filters.CharFilter(method='get_address')
    day = filters.ModelMultipleChoiceFilter(
        field_name='schedule__day',  # Используйте schedule__day вместо day
        queryset=DayOfWeek.objects.all()
    )
    time_range = filters.CharFilter(method='get_time_range')

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group', 'price', 'address', 'day', 'time_range')

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

    # Фильтр по времени
    def get_time_range(self, queryset, name, value):
        time_from, time_until = map(str.strip, value.split('-'))

        queryset = queryset.filter(
            schedule__time_from__gte=time_from,
            schedule__time_until__lte=time_until
        )
        return queryset


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""

    class Meta:
        model = SportType
        fields = ('title', )
