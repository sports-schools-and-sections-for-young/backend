from django.test import TestCase
from organizations.models import SportOrganization
from rest_framework.test import APIClient
from sections.models import DayOfWeek, Section, SportType
from users.models import CustomUser


class ViewsunauthorizedTest(TestCase):
    def setUp(self):
        self.guest_client = APIClient()

    def test_sport_type_list_url(self):
        response = self.guest_client.get('/api/sport_types/')
        self.assertEqual(response.status_code, 200)

    def test_search_section_list_url(self):
        response = self.guest_client.get('/api/search_sections/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        data = {
            "email": "test@yandex.ru",
            "password": "1456testd",
            "check_password": "1456testd"
        }
        response = self.guest_client.post('/api/register/', data)
        resp_data = response.json()
        self.assertEqual(list(resp_data.keys()), ['email'])
        self.assertEqual(response.status_code, 201)


class ViewsTestAuthenticated(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)

    def test_login_user(self):
        data = {
            "email": "test@yandex.ru",
            "password": 'test14536'
        }
        response = self.guest_client.post('/api/login/', data)
        self.assertEqual(response.status_code, 200)

    def test_del_user(self):
        data = {
            'current_password': 'test14536'
        }
        response = self.guest_client.delete('/api/user/delete/', data)
        self.assertEqual(response.status_code, 204)

    def test_sport_type_create(self):
        data = {
            'title': 'Tests'
        }
        response = self.guest_client.post('/api/create_sport_types/',
                                          data)
        self.assertEqual(response.status_code, 201)

    def test_sport_organization_create(self):
        data = {
            "title": "Testy",
            "user": self.guest_client,
            "address": "test",
            "email": "test@mail.ru",
            "phone": 125469874563289
        }
        response = self.guest_client.post('/api/create_sport_organization/',
                                          data)
        self.assertEqual(response.status_code, 201)


class SportOrganizationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.sport_organization = SportOrganization.objects.create(
            title="Test",
            user=self.user,
            address="test",
            email="test@mail.ru",
            phone=125469874563289
        )
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)

    def test_sportorganizations_patch(self):
        data = {
            "title": "Test_test"
        }
        response = self.guest_client.patch('/api/sport_school/update/', data)
        self.assertEqual(response.status_code, 200)


class SectionViewsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.sport_organization = SportOrganization.objects.create(
            title="Test",
            user=self.user,
            address="test",
            email="test@mail.ru",
            phone=125469874563289,
            id=1
        )
        self.sport_type = SportType.objects.create(
            title='test'
        )
        self.days = DayOfWeek.objects.create(title='tests', id=1)
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)

    def test_create_section(self):
        data = {
            'title': 'Testt',
            'gender': '',
            'sport_type': 1,
            'price': 100,
            'year_from': 3,
            'year_until': 10,
            'free_class': 'False',
            'address': 'test',
            'schedule': (1, ),
            'latitude': '1',
            'longitude': '1'

        }
        response = self.guest_client.post('/api/create_section/', data)
        self.assertEqual(response.status_code, 201)


class SectionViewsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.sport_organization = SportOrganization.objects.create(
            title="Test",
            user=self.user,
            address="test",
            email="test@mail.ru",
            phone=125469874563289,
            id=1
        )
        self.sport_type = SportType.objects.create(
            title='test', id=1
        )
        self.days = DayOfWeek.objects.create(title='tests', id=1)
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)

    def test_create_section(self):
        data = {
            'title': 'Testt',
            'sport_type': 1,
            'price': 0,
            'gender': 'Man',
            'latitude': 1,
            'longitude': 1,
            'year_from': 3,
            'year_until': 10,
            'address': 'test',
            'free_class': True,
            'schedule': [1, ]

        }
        response = self.guest_client.post('/api/create_section/', data)
        self.assertEqual(response.status_code, 201)


class SectionUpdateDeleteTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.sport_organization = SportOrganization.objects.create(
            title="Test",
            user=self.user,
            address="test",
            email="test@mail.ru",
            phone=125469874563289,
            id=1
        )
        self.sport_type = SportType.objects.create(
            title='test'
        )
        self.days = DayOfWeek.objects.create(title='tests', id=1)
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)
        self.section = Section.objects.create(
            sport_organization=self.sport_organization,
            title='Testt',
            id=1,
            sport_type=self.sport_type,
            price=0,
            year_from=3,
            year_until=10,
            address='test'
        )
        self.section.schedule.add(self.days)
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)

    def test_section_update(self):
        data = {
            'title': 'Test_test'
        }
        response = self.guest_client.patch('/api/section/1/update/', data)
        self.assertEqual(response.status_code, 200)

    def test_section_delete(self):
        response = self.guest_client.delete('/api/section/1/delete/')
        self.assertEqual(response.status_code, 204)


class ProfileTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)
        self.sport_organization = SportOrganization.objects.create(
            title="Test",
            user=self.user,
            address="test",
            email="test@mail.ru",
            phone=125469874563289,
            id=1
        )

    def test_profile_get(self):
        response = self.guest_client.get('/api/sport_school/')
        self.assertEqual(response.status_code, 200)


class SportTypeTest(TestCase):
    def setUp(self):
        self.sport_type = SportType.objects.create(
            title="Testf"
        )
        self.user = CustomUser.objects.create_user(email='test@yandex.ru',
                                                   password='test14536',
                                                   username="test",
                                                   id=1)
        self.user.save()
        self.guest_client = APIClient()
        self.guest_client.force_authenticate(user=self.user)

    def test_sport_type_list(self):
        response = self.guest_client.get('/api/sport_types/')
        self.assertEqual(response.status_code, 200)
