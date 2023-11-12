from rest_framework import serializers
from sections.models import SportType
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


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для секций: вид спорта, пол, адрес, цена."""

    class Meta:
        models = Section
        fields = ['sport_type', 'age_group', 'gender',
                  'address', 'aviable', 'price', ]


class SheduleSerializer(serializers.ModelSerializer):
    """Сериалализатор для расписания."""

    class Meta:
        model = Shedule
        fields = '__all__'


class RewievSerializer(serializers.ModelSerializer):
    """Сериализатор для рейтинга."""

    class Meta:
        model = Rewiev
        models = ['rating', 'sport_school']


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


class SportOrganizationSerializer(serializers.ModelSerializer):
    """Сериализатор для спртивных организаций(вспомогательный)."""

    class Meta:
        model = SportOrganization
        fields = ['title', 'address']
