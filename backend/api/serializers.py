from django.db.models import Avg
from organizations.models import Review
from rest_framework import serializers
from sections.models import Address, AgeGroup, Schedule, Section, SportType


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
    rating = serializers.SerializerMethodField()
    review_amount = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

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


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'
