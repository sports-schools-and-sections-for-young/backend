from django.db.models import Avg
from haversine import haversine
from organizations.models import Review
from rest_framework import serializers
from sections.models import (Address, AgeGroup, PhoneOfSection, Schedule,
                             Section, SportType)
import math


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


class RewievSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга."""

    class Meta:
        model = Review
        fields = ['rating']


class AgeGroupSerializer(serializers.ModelSerializer):
    """Сериализатор для возрастной группы(вспомагательный)."""

    class Meta:
        model = AgeGroup
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    """Сериалализатор для расписания."""

    class Meta:
        model = Schedule
        fields = '__all__'


class ShortSectionSerializer(serializers.ModelSerializer):
    """Сериализатор для выдаче полей в поиске."""
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    location = serializers.ReadOnlyField(source='address.location')
    distance = serializers.SerializerMethodField()
    sport_organization = serializers.ReadOnlyField(
        source='sport_organization.title'
    )

    class Meta:
        model = Section
        fields = ['sport_organization', 'rating', 'rating_count', 'location',
                  'distance']

    def get_rating(self, obj):
        rating = Review.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.aggregate(Avg('rating'))['rating__avg']

    def get_rating_count(self, obj):
        rating = Review.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.count()

    def get_distance(self, obj):
        request = self.context['request']
        location = request.query_params.get('location')
        lat, lon = location.split(',')
        lat = float(lat)
        lon = float(lon)
        location_1 = obj.address.location
        lat_1, lon_1 = location_1.split(',')
        lat_1 = float(lat_1)
        lon_1 = float(lon_1)
        earth_radius = 6371
        lat1_rad = math.radians(lat_1)
        lon1_rad = math.radians(lon_1)
        lat2_rad = math.radians(lat)
        lon2_rad = math.radians(lon)
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(
            lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
        return distance


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для секций: вид спорта, пол, адрес, цена."""
    sport_type = serializers.ReadOnlyField(source='sport_type.title')
    age_group = AgeGroupSerializer()
    shedule = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['sport_type', 'age_group', 'gender', 'aviable', 'price',
                  'section', 'shedule']

    def get_shedule(self, obj):
        shedules = Schedule.objects.filter(section=obj)
        day = []
        for shedule in shedules:
            day = ' '.join(day.title for day in shedule.day.all())
        return {'day': day}

    def haversine(self, lat1, lon1, lat2, lon2):
        earth_radius = 6371
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(
            lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
        return distance

    def get_section(self, obj):
        section = Section.objects.all()
        request = self.context['request']
        radius = request.query_params.get('radius')
        location = request.query_params.get('location')
        section_list = []
        for i in section:
            section_list.append(i)
        lat, lon = location.split(',')
        lon = float(lon)
        lat = float(lat)
        radius = int(radius)
        for obj in section:
            lat_1, lon_1 = (obj.address.location).split(',')
            lat_1 = float(lat_1)
            lon_1 = float(lon_1)
            distance = self.haversine(lat, lon, lat_1, lon_1)
            if distance <= radius:
                section_list.append(obj)
        serializer = ShortSectionSerializer(section_list,
                                            context={'request': request},
                                            many=True)
        return serializer.data
