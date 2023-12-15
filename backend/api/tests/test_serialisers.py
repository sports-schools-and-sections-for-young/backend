from django.test import TestCase, RequestFactory
from rest_framework import serializers

from api.serializers import (
    SportTypeCreateSerializer,
    RegisterSerializer,
    SportOrganizationCreateSerializer
)
from sections.models import SportType
from organizations.models import SportOrganization
from users.models import CustomUser


class SportTypeSerializerTest(TestCase):

    def test_create_valid_data(self):
        serializer = SportTypeCreateSerializer(data={'title': 'Football'})
        serializer.is_valid()
        instance = serializer.save()

        self.assertEqual(instance.title, 'Football')
        self.assertTrue(SportType.objects.filter(title='Football').exists())

    def test_create_invalid_title_not_start_with_capital_letter(self):
        serializer = SportTypeCreateSerializer(data={'title': 'football'})
        if serializer.is_valid():
            with self.assertRaises(serializers.ValidationError):
                serializer.save()

    def test_double_sport_type(self):
        SportType.objects.create(title='Football')
        serializer = SportTypeCreateSerializer(data={'title': 'Football'})
        if serializer.is_valid():
            with self.assertRaises(serializers.ValidationError):
                serializer.save()


class RegisterSerializerTest(TestCase):
    def test_valid_password(self):
        serializer = RegisterSerializer(data={"password": "300613test",
                                              "check_password": "300613tes"})
        if serializer.is_valid():
            with self.assertRaises(serializers.ValidationError):
                serializer.save()

    def test_register_user_exists(self):
        serializer = RegisterSerializer(data={
            "email": "test@yandex.ru",
            "password": "test123456",
            "check_password": "test123456"
        })
        serializer.is_valid()
        user = serializer.save()
        self.assertTrue(user.email, "test@yandex.ru")
        self.assertTrue(CustomUser.objects.filter(email="test@yandex.ru"
                                                  ).exists())


class SportOrganizationCreateSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create(email='test@example.com',
                                              password='ytrst124563')
        self.request = self.factory.get('/dummy/url/')
        self.request.user = self.user
        self.data = {
            'title': 'Testhtf',
            'address': 'test',
            'email': 'info@yandex.com',
            'phone': '1234567890h',
        }

    def test_create_invalid_duplicate_organization(self):
        SportOrganization.objects.create(title='Testjnv',
                                         user=self.user)
        serializer_context = {'request': self.request}
        serializer = SportOrganizationCreateSerializer(
            data=self.data,
            context=serializer_context
        )
        if serializer.is_valid():
            with self.assertRaises(serializers.ValidationError):
                serializer.save()
