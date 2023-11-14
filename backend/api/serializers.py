import math
from rest_framework import serializers
from django.db.models import Avg

from sections.models import (
    Section,
    Shedule,
    AgeGroup,
    SportType
)
from organizations.models import Rewiev, Address


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'


class RewievSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга."""

    class Meta:
        model = Rewiev
        fields = ['rating']


class AgeGroupSerializer(serializers.ModelSerializer):
    """Сериализатор для возрастной группы(вспомагательный)."""

    class Meta:
        model = AgeGroup
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    """ Сериализер для адреса спорт-школы(вспомогательный)."""

    class Meta:
        model = Address
        fields = ['street', 'house', 'location']


class SheduleSerializer(serializers.ModelSerializer):
    """Сериалализатор для расписания."""

    class Meta:
        model = Shedule
        fields = '__all__'


class ShortSectionSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    location = serializers.ReadOnlyField(source='address.location')

    class Meta:
        model = Section
        fields = ['title', 'rating', 'rating_count', 'location']

    def get_rating(self, obj):
        rating = Rewiev.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.aggregate(Avg('rating'))['rating__avg']

    def get_rating_count(self, obj):
        rating = Rewiev.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.count()


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для секций: вид спорта, пол, адрес, цена."""
    # location = serializers.ReadOnlyField(source='address.location')
    sport_type = serializers.ReadOnlyField(source='sport_type.title')
    age_group = AgeGroupSerializer()
    # rating = serializers.SerializerMethodField()
    # rating_count = serializers.SerializerMethodField()
    address = AddressSerializer()
    shedule = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['sport_type', 'age_group', 'gender', 'aviable', 'price',
                  'address', 'section', 'shedule']

    def get_shedule(self, obj):
        shedules = Shedule.objects.filter(section=obj)
        day = []
        for shedule in shedules:
            day = ' '.join(day.title for day in shedule.day.all())
        return {'day': day}

    def haversine(lat1, lon1, lat2, lon2):
        earth_radius = 6371
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
        return distance

    def get_section(self, obj):
        section = Section.objects.all()
        request = self.context['request']
        radius = request.query_params.get('radius')
        location = request.query_params.get('location')
        # print(request)
        section_list = []
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
        return section_list

    def to_representation(self, instance):
        return ShortSectionSerializer(
            instance, context={'request': self.context.get('request')}).data
