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

    class Meta:
        model = Section
        fields = '__all__'


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'
