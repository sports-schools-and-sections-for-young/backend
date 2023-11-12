from rest_framework import serializers
from sections.models import SportType
from django.db.models import Avg, Count
# from rest_framework.validators import (
#     UniqueTogetherValidator,
#     UniqueForYearValidator
# )

from sections.models import (
    Section,
    Shedule,
    AgeGroup,
    SportType
)
from organizations.models import Rewiev, Address, SportOrganization


# class CoordinatSerializer(serializers.ModelSerializer):
#     """Сериаоизаатор для координат."""

#     class Meta:
#         model = Location
#         fields = '__all__'


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


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для секций: вид спорта, пол, адрес, цена."""
    # location = serializers.ReadOnlyField(source='address.location')
    sport_type = serializers.ReadOnlyField(source='sport_type.title')
    age_group = AgeGroupSerializer()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    address = AddressSerializer()

    class Meta:
        model = Section
        fields = ['sport_type', 'age_group', 'gender', 'aviable', 'price',
                  'address', 'rating', 'rating_count']

    def get_rating(self, obj):
        rating = Rewiev.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.aggregate(Avg('rating'))['rating__avg']

    def get_rating_count(self, obj):
        rating = Rewiev.objects.filter(sport_school=obj.sport_organization)
        if rating.exists():
            return rating.count()


class SearchSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    sport_organization = serializers.ReadOnlyField()

    class Meta:
        model = Section
        fields = ['sport_organization', 'rating']


class SheduleSerializer(serializers.ModelSerializer):
    """Сериалализатор для расписания."""

    class Meta:
        model = Shedule
        fields = '__all__'



# class SportOrganizationSerializer(serializers.ModelSerializer):
#     """Сериализатор для спртивных организаций(вспомогательный)."""

#     class Meta:
#         model = SportOrganization
#         fields = ['title', 'address']
