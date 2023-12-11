from django.db import transaction
from django.test import TestCase

from organizations.models import (
    SportOrganization,
    PhoneNumber
)
from sections.models import (
    DayOfWeek,
    Section,
    SportType
)


class SportOrganizationModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sportorganization = SportOrganization.objects.create(
            title='Dgj',
            email='inf',
            address='test',
            description='test'
        )

    def test_title_length(self):
        sportorganization = SportOrganizationModelTest.sportorganization
        title_length = sportorganization._meta.get_field('title').validators[0]
        message = title_length.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_email_length(self):
        sportorganization = SportOrganizationModelTest.sportorganization
        email_length = sportorganization._meta.get_field('email').validators[0]
        message = email_length.message
        self.assertEqual(message,
                         'Введите правильный адрес электронной почты.')


class PhoneNumberModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_value_length(self):
        phone = PhoneNumber.objects.create(value=123456)
        phone_length = phone._meta.get_field('value').validators[0]
        message = phone_length.message
        self.assertEqual(message, 'Минимум 14 символов')


class DayOfWeekModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_title__day_min(self):
        day = DayOfWeek.objects.create(title='hg')
        day_min = day._meta.get_field('title').validators[0]
        message = day_min.message
        self.assertEqual(message, 'Минимум 5 символов')


class SectionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sportorganization = SportOrganization.objects.create(
            title='Dgj',
            email='test@yandex.ru',
            address='test',
            description='test'
        )
        cls.sport_type = SportType.objects.create(
            title='Test'
        )
        cls.days = DayOfWeek.objects.bulk_create(
            [DayOfWeek(title='понедельник'),
             DayOfWeek(title='вториник')])
        with transaction.atomic():
            cls.section = Section.objects.create(
                title='Ghj',
                aviable=1000,
                sport_organization=cls.sportorganization,
                # schedule=cls.days,
                year_from=2,
                year_until=19,
                sport_type=cls.sport_type,
                price=1000000,
                address='test',
                latitude=24.2589454,
                longitude=28.2547899
            )
            cls.section.schedule.set(cls.days)

    def test_year_until_min(self):
        year_until = SectionModelTest.section
        year_until.year_until = 2
        year_until_min = year_until._meta.get_field('year_until').validators[0]
        message = year_until_min.message
        self.assertEqual(message, 'Минимальное значение 3')

    def test_year_from_min(self):
        year_from = SectionModelTest.section
        year_from_min = year_from._meta.get_field('year_from').validators[0]
        message = year_from_min.message
        print(year_from_min)
        self.assertEqual(message, 'Минимальное значение 3')

    def test_year_until_max(self):
        year_until = SectionModelTest.section
        year_until_max = year_until._meta.get_field('year_until').validators[1]
        message = year_until_max.message
        print(year_until_max)
        self.assertEqual(message, 'Максимальное значение 18')

    def test_year_from_max(self):
        year_from = SectionModelTest.section
        year_from.year_from = 18
        year_from_max = year_from._meta.get_field('year_from').validators[1]
        message = year_from_max.message
        self.assertEqual(message, 'Максимальное значение 18')
