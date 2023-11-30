from django.test import TestCase
from api.serializers import (
    SportTypeSerializer
)


class TestSportTypeSerializer(TestCase):

    def test_sport_type_serializer(self):
        valid_data = {
            'title': 'test'
        }
        serializer = SportTypeSerializer(data=valid_data)
        serializer.is_valid()
        model_instance = serializer.save()
        self.assertEqual(model_instance.title, valid_data['title'])
