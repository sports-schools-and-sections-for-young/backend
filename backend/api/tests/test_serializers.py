from django.test import TestCase
from api.serializers import SportTypeCreateSerializer
from sections.models import SportType


class SportTypeCreateSerializerTestCase(TestCase):
    def test_serializer_valid_data(self):
        # Проверка сериализации с корректными данными
        data = {
            'title': 'Football'
        }
        serializer = SportTypeCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # Проверка создания видов спорта
        sport_type = serializer.save()
        self.assertEqual(sport_type.title, 'Football')

    # def test_serializer_invalid_title(self):
    #     # Проверка сериализации с некорректными данными (заглавная буква)
    #     data = {
    #         'title': 'basketball'
    #     }
    #     serializer = SportTypeCreateSerializer(data=data)
    #     serializer.is_valid()
    #     print(serializer)
    #     # self.assertTrue(serializer.is_valid())
    #     self.assertIn('Название вида спорта должно начинаться с заглавной'
    #                   'буквы!', serializer)

    # def test_serializer_invalid_characters(self):
    #     # Проверка сериализации с некорректными данными (символы)
    #     data = {
    #         'title': 'Basketball 123'
    #     }
    #     serializer = SportTypeCreateSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('Название вида спорта должно содержать только буквы!',
    # serializer.errors['title'])

    # def test_serializer_duplicate_title(self):
    #     # Проверка сериализации с некорректными данными (дубликат)
    #     data = {
    #         'title': 'Football'
    #     }
    #     SportType.objects.create(title='Football')
    #     serializer = SportTypeCreateSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('Такой вид спорта уже существует!',
    # serializer.errors['title'])
