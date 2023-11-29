from django.db.models import Avg
from haversine import haversine
from organizations.models import Review
from rest_framework import serializers
from sections.models import (Address, AgeGroup, PhoneOfSection, Schedule,
                             Section, SportType)


class AgeGroupSerializer(serializers.ModelSerializer):
    """Сериализатор для возрастной группы."""

    class Meta:
        model = AgeGroup
        fields = ('year_from', 'year_until')


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор для адреса секции или спортшколы."""

    class Meta:
        model = Address
        fields = ('index', 'city', 'metro', 'district', 'street', 'house')


class SearchSectionSerializer(serializers.ModelSerializer):
    """Сериализатор для поиска секций."""
    sport_organization = serializers.CharField(
        source='sport_organization.title'
    )
    sport_type = serializers.CharField(source='sport_type.title')
    site = serializers.CharField(source='sport_organization.site')
    age_group = AgeGroupSerializer()
    address = AddressSerializer()
    # На данный момент, у нас не будет личного кабинета пользователя,
    # поэтому не будет отзывов и рейтинга секций
    # rating = serializers.SerializerMethodField()
    # review_amount = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    latitude = serializers.CharField(source='address.latitude')
    longitude = serializers.CharField(source='address.longitude')

    class Meta:
        model = Section
        fields = '__all__'

    # Подсчет среднего рейтинга спортшколы
    def get_rating(self, obj):
        rating = Review.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            rating_avg = rating.aggregate(Avg('rating'))['rating__avg']
            return round(rating_avg, 2)

    # Подсчет количества отзывов
    def get_review_amount(self, obj):
        return Review.objects.filter(
            sport_school=obj.sport_organization
        ).count()

    # Отображение расписания секции
    def get_schedule(self, obj):
        schedules = Schedule.objects.filter(section=obj)
        days_of_week = []
        times = ""
        for schedule in schedules:
            days_of_week = ', '.join([day.title for day in schedule.day.all()])
            times = (f"{schedule.time_from.strftime('%H:%M')} - "
                     f"{schedule.time_until.strftime('%H:%M')}")
        return {'days': days_of_week, 'time': times}

    # Получение телефона секции
    def get_phone_of_section(self, obj):
        return PhoneOfSection.objects.filter(section=obj).first()

    # Отображение телефона секции
    def get_phone(self, obj):
        phone_of_section = self.get_phone_of_section(obj)
        return phone_of_section.phone.value

    # Отображение комментария к телефону секции
    def get_comment(self, obj):
        phone_of_section = self.get_phone_of_section(obj)
        return phone_of_section.phone.comment

    # Отображение расстояния от пользователя до секции
    def get_distance(self, obj):
        # Координаты по-умолчанию None, чтобы не сломался эндпойнт, если
        # координаты не были переданы
        coords = self.context.get('request').query_params.get('coords', None)
        if coords is not None:
            # Получение широты и долготы пользователя
            user_lat, user_lon = map(float, coords.split(':'))
            # Получение широты и долготы секции
            section_lat = obj.address.latitude
            section_lon = obj.address.longitude
            # Координаты пользователя
            user_coords = (user_lat, user_lon)
            # Координаты секции
            section_coords = (section_lat, section_lon)
            # Расчет расстояния
            distance = haversine(user_coords, section_coords)
            return round(distance, 2)


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'
