from rest_framework import serializers
from sections.models import SportType


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'
