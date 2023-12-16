from django_filters.rest_framework import FilterSet, filters
from haversine import haversine
from sections.models import DayOfWeek, Section, SportType


class SearchSectionFilter(FilterSet):
    """
    Фильтр для поиска секций по следующим полям: пол ребенка, вид спорта,
    возраст ребенка, стоимость занятий, дням работы секции, расстоянию до
    секции.
    """
    age_group = filters.NumberFilter(
        label='Возраст ребенка',
        method='get_age_group'
    )
    sport_type = filters.ModelMultipleChoiceFilter(
        label='Вид спорта',
        queryset=SportType.objects.all(),
        field_name='sport_type__title',
        to_field_name='title'
    )
    price = filters.NumberFilter(method='get_price')
    schedule = filters.ModelMultipleChoiceFilter(
        label='День недели',
        queryset=DayOfWeek.objects.all(),
        field_name='schedule__title',
        to_field_name='title'
    )
    distance = filters.NumberFilter(
        label='Поиск по расстоянию',
        method='get_distance'
    )

    class Meta:
        model = Section
        fields = ('gender', 'sport_type', 'age_group', 'price', 'schedule',
                  'free_class')

    # Фильтр по возрасту ребенка
    def get_age_group(self, queryset, name, value):
        return queryset.filter(year_until__gte=value, year_from__lte=value)

    # Фильтр по стоимости занятий
    def get_price(self, queryset, name, value):
        return queryset.filter(price__gte=0, price__lte=value)

    # Фильтр по расстоянию
    def get_distance(self, queryset, name, value):
        # Координаты по-умолчанию None, чтобы эндпойнт не сломался, если
        # координаты не были переданы
        coords = self.request.query_params.get('coords', None)
        if coords:
            # Получение широты и долготы пользователя
            user_lat, user_lon = map(float, coords.split(':'))
            # Координаты пользователя
            user_coords = (user_lat, user_lon)
            # Список, который содержит секции отфильтрованные по расстоянию
            filtered_sections = []
            # Перебираем все объекты модели Section
            for section in queryset:
                # Получение широты и долготы секции
                section_lat = section.latitude
                section_lon = section.longitude
                # Координаты секции
                section_coords = (section_lat, section_lon)
                # Расчет расстояния
                distance = haversine(user_coords, section_coords)
                # Фильруем по расстоянию
                if distance <= value:
                    filtered_sections.append(section.id)
            return queryset.filter(id__in=filtered_sections)
        return queryset


class SportTypeFilter(FilterSet):
    """Фильтр по видам спорта."""

    class Meta:
        model = SportType
        fields = ('title', )
