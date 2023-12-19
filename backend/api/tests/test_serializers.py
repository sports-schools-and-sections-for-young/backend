from unittest.mock import Mock

from api.serializers import (RegisterSerializer, SearchSectionSerializer,
                             SportOrganizationCreateSerializer,
                             SportTypeCreateSerializer)
from django.test import RequestFactory, TestCase
from haversine import haversine
from organizations.models import SportOrganization
from rest_framework import serializers
from sections.models import DayOfWeek, Section, SportType
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


class SearchSectionSeriializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(email='teat@example.com',
                                             password='test_142355', id=1)
        cls.sport_organ = SportOrganization.objects.create(id=1, user=cls.user)
        cls.section = Section.objects.create(
            id=1,
            year_from=3,
            year_until=5,
            sport_organization_id=cls.sport_organ.id,
            latitude=45.035432,
            longitude=38.972977)
        day_1 = DayOfWeek.objects.create(title='Monday')
        day_2 = DayOfWeek.objects.create(title='Thuesday')
        cls.section.schedule.add(day_1, day_2)

    def test_age_group_test(self):
        data = {
            'year_from': 3,
            'year_until': 7
        }
        section = Section(**data)
        serializer = SearchSectionSerializer()
        result = serializer.get_age_group(section)

        self.assertEqual(result, {
            "year_from": 3,
            "year_until": 7,
        })

    def test_get_schedule(self):
        serializer = SearchSectionSerializer()
        result = serializer.get_schedule(SearchSectionSeriializerTest.section)
        expected_schedule = 'Monday, Thuesday'
        self.assertEqual(result, expected_schedule)

    def test_get_distance(self):
        mock_request = Mock()
        mock_query_params = {'coords': '45.027483:38.971181'}
        mock_request.query_params = mock_query_params
        self.context = {'request': mock_request}
        coords = self.context['request'].query_params.get('coords')
        user_lat, user_lon = map(float, coords.split(':'))
        user_coords = (user_lat, user_lon)
        obj = SearchSectionSeriializerTest.section
        section_coords = (obj.latitude, obj.longitude)
        serializer = SearchSectionSerializer(context=self.context)
        result = serializer.get_distance(obj)
        expected_distance = haversine(user_coords, section_coords)
        self.assertEqual(result, round(expected_distance, 2))
