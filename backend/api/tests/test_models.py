from django.test import TestCase

from organizations.models import (
    Address,
    SportOrganization,
    Review,
    PhoneNumber
)

from sections.models import (
    AgeGroup,
    Section,
    DayOfWeek,
    SportType
)
from users.models import CustomUser


class AddressModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address = Address.objects.create(
            index='191a0',
            city='С',
            metro='Чка',
            district='Пет',
            street='Чка',
            house='16B',
            full_address='afgklfl',
            latitude=50.254789,
            longitude=39.254789

        )

    def test_of_index_structure(self):
        address = AddressModelTest.address
        index = address._meta.get_field('index').validators[0]
        message = index.message
        self.assertEqual(message, 'Минимум 6 символов')

    def test_index_min_regex(self):
        address = AddressModelTest.address
        structure = address._meta.get_field('index').validators[1]
        message = structure.message
        self.assertEqual(message, 'Индекс может содержать только цифры.')

    def test_city_length(self):
        address = AddressModelTest.address
        city_length = address._meta.get_field('city').validators[0]
        message = city_length.message
        self.assertEqual(message, 'Минимум 2 символа')

    def test_metro_length(self):
        address = AddressModelTest.address
        metro_length = address._meta.get_field('metro').validators[0]
        message = metro_length.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_district_length(self):
        address = AddressModelTest.address
        district_length = address._meta.get_field('metro').validators[0]
        message = district_length.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_street_length(self):
        address = AddressModelTest.address
        street_length = address._meta.get_field('street').validators[0]
        message = street_length.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_house_length(self):
        address = AddressModelTest.address
        house_length = address._meta.get_field('house').validators[0]
        message = house_length.message
        self.assertEqual(message, 'Минимум 1 символ')


class SportOrganizationModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address = Address.objects.create(
            index='191a0',
            city='С',
            metro='Чка',
            district='Пет',
            street='Чка',
            house='16B',
            full_address='afgklfl',
            latitude=50.254789,
            longitude=39.254789
        )
        cls.sportorganization = SportOrganization.objects.create(
            title='Dgj',
            email='inf',
            address=cls.address,
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


class ReviewTestModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address = Address.objects.create(
            index='191a0',
            city='С',
            metro='Чка',
            district='Пет',
            street='Чка',
            house='16B',
            full_address='afgklfl',
            latitude=50.254789,
            longitude=39.254789
        )
        cls.sportorganization = SportOrganization.objects.create(
            title='Dgj',
            email='inf',
            address=cls.address,
            description='test'
        )
        cls.review = Review.objects.create(
            sport_school=cls.sportorganization,
            rating=0
        )

    def test_rating_min(self):
        review = ReviewTestModel.review
        review_min = review._meta.get_field('rating').validators[0]
        message = review_min.message
        self.assertEqual(message, 'Минимумальное значение 1')

    def test_rating_max(self):
        review = ReviewTestModel.review
        review.rating = 10
        review_max = review._meta.get_field('rating').validators[1]
        message = review_max.message
        self.assertEqual(message, 'Максимальное значение 5')


class PhoneNumberModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_value_length(self):
        phone = PhoneNumber.objects.create(value=123456)
        phone_length = phone._meta.get_field('value').validators[0]
        message = phone_length.message
        self.assertEqual(message, 'Минимум 14 символов')


class AgeGroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.age = AgeGroup.objects.create(
            year_from=0,
            year_until=100
        )

    def test_year_from_min(self):
        year_from = AgeGroupModelTest.age
        year_from_min = year_from._meta.get_field('year_from').validators[0]
        message = year_from_min.message
        print(year_from_min)
        self.assertEqual(message, 'Минимальное значение 1')

    def test_year_until_max(self):
        year_until = AgeGroupModelTest.age
        year_until_max = year_until._meta.get_field('year_until').validators[1]
        message = year_until_max.message
        print(year_until_max)
        self.assertEqual(message, 'Максимальное значение 99')

    def test_year_from_max(self):
        year_from = AgeGroupModelTest.age
        year_from.year_from = 100
        year_from_max = year_from._meta.get_field('year_from').validators[1]
        message = year_from_max.message
        self.assertEqual(message, 'Максимальное значение 99')

    def test_year_until_min(self):
        year_until = AgeGroupModelTest.age
        year_until.year_until = 0
        year_until_min = year_until._meta.get_field('year_until').validators[0]
        message = year_until_min.message
        self.assertEqual(message, 'Минимальное значение 1')


class SectionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.address = Address.objects.create(
            index='191a0',
            city='С',
            metro='Чка',
            district='Пет',
            street='Чка',
            house='16B',
            full_address='afgklfl',
            latitude=50.254789,
            longitude=39.254789
        )
        cls.age = AgeGroup.objects.create(
            year_from=0,
            year_until=100
        )
        cls.sportorganization = SportOrganization.objects.create(
            title='Dgj',
            email='inf',
            address=cls.address,
            description='test'
        )
        cls.sport_type = SportType.objects.create(
            title='Test'
        )
        cls.section = Section.objects.create(
            title='Ghj',
            aviable=1000,
            sport_organization=cls.sportorganization,
            sport_type=cls.sport_type,
            price=1000000,
            address=cls.address,
            age_group=cls.age
        )

    def test_title_min(self):
        section = SectionModelTest.section
        title_min = section._meta.get_field('title').validators[0]
        message = title_min.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_aviable_max(self):
        section = SectionModelTest.section
        aviable_max = section._meta.get_field('aviable').validators[0]
        message = aviable_max.message
        self.assertEqual(message, 'Максимальное значение 999')


class DayOfWeekModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_title__day_min(self):
        day = DayOfWeek.objects.create(title='hg')
        day_min = day._meta.get_field('title').validators[0]
        message = day_min.message
        self.assertEqual(message, 'Минимум 5 символов')


class CustomUserTestModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(
            email='test',
            username='тест'
        )

    def test_username_length(self):
        user = CustomUserTestModel.user
        username_length = user._meta.get_field('username').validators[0]
        message = username_length.message
        self.assertEqual(message, 'Минимум 5 символов')

    def test_username_structure(self):
        user = CustomUserTestModel.user
        username_structure = user._meta.get_field('username').validators[1]
        message = username_structure.message
        self.assertEqual(message, 'Логин может содержать только символы '
                         'английского алфавита и цифры.')
