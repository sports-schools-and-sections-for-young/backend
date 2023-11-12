from django.db.models import Avg
from organizations.models import Review
from rest_framework import serializers
from sections.models import Address, AgeGroup, Section, SportType


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
    age_group = AgeGroupSerializer()
    address = AddressSerializer()
    rating = serializers.SerializerMethodField()
    review_amount = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = '__all__'

    # Подсчет среднего рейтинга спортшколы
    def get_rating(self, obj):
        rating = Review.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.aggregate(Avg('rating'))['rating__avg']

    # Подсчет количества отзывов
    def get_review_amount(self, obj):
        return Review.objects.filter(
            sport_school=obj.sport_organization
        ).count()


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'
