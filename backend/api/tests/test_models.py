from django.test import TestCase

from organizations.models import SportOrganization
from sections.models import SportType, DayOfWeek, Section
from users.models import CustomUser


class SportOrganizationModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(
            email='test@yandex.ru',
            password='test12345'
        )
        cls.sportorganiz = SportOrganization.objects.create(
            user=cls.user,
            title='test',
            address='test',
            email='t.ru',
            phone='12345678'
        )

    def test_title_length(self):
        sportorg = SportOrganizationModelTest.sportorganiz
        title = sportorg._meta.get_field('title').validators[0]
        message = title.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_email_length(self):
        sportorg = SportOrganizationModelTest.sportorganiz
        email = sportorg._meta.get_field('email').validators[0]
        message = email.message
        self.assertEqual(message,
                         'Введите правильный адрес электронной почты.')

    def test_phone_length(self):
        sportorg = SportOrganizationModelTest.sportorganiz
        phone = sportorg._meta.get_field('phone').validators[0]
        message = phone.message
        self.assertEqual(message, 'Минимум 14 символов')


class DayOfWeekTestModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.days = DayOfWeek.objects.create(
            title='test'
        )

    def test_title_length(self):
        days = DayOfWeekTestModel.days
        days_val = days._meta.get_field('title').validators[0]
        message = days_val.message
        self.assertEqual(message, 'Минимум 5 символов')


class SectionTestModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(
            email='test1@yandex.ru',
            password='test12345'
        )
        cls.sportorganiz = SportOrganization.objects.create(
            user=cls.user,
            title='tes1t',
            address='test',
            email='t2.ru',
            phone='12345678'
        )
        cls.sport_type = SportType.objects.create(
            title='test'
        )
        cls.days = DayOfWeek.objects.create(
            title='test'
        )
        cls.section = Section.objects.create(
            title='Ghj',
            sport_organization=cls.sportorganiz,
            sport_type=cls.sport_type,
            price=10000,
            address='test',
            year_from=2,
            year_until=19
        )

    def test_title_min(self):
        section = SectionTestModels.section
        title_min = section._meta.get_field('title').validators[0]
        message = title_min.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_year_from_min(self):
        year_from = SectionTestModels.section
        year_from_min = year_from._meta.get_field('year_from').validators[0]
        message = year_from_min.message
        print(year_from_min)
        self.assertEqual(message, 'Минимальное значение 3')

    def test_year_until_max(self):
        year_until = SectionTestModels.section
        year_until_max = year_until._meta.get_field('year_until').validators[1]
        message = year_until_max.message
        print(year_until_max)
        self.assertEqual(message, 'Максимальное значение 18')

    def test_year_from_max(self):
        year_from = SectionTestModels.section
        year_from.year_from = 19
        year_from_max = year_from._meta.get_field('year_from').validators[1]
        message = year_from_max.message
        self.assertEqual(message, 'Максимальное значение 18')

    def test_year_until_min(self):
        year_until = SectionTestModels.section
        year_until.year_until = 2
        year_until_min = year_until._meta.get_field('year_until').validators[0]
        message = year_until_min.message
        self.assertEqual(message, 'Минимальное значение 3')


class UserTestModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(
            email='test@yandex.ru',
            password='test'
        )
        cls.user.save()

    def test_password_length(self):
        user = UserTestModel.user
        password = user._meta.get_field('password').validators[0]
        message = password.message
        self.assertEqual(message, 'Минимум 8 символов')

    def test_save_user(self):
        user = UserTestModel.user
        self.assertIsNotNone(user.username)
        self.assertTrue(user.username.isalnum())
