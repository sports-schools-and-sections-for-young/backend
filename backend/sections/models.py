from django.conf import settings
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from organizations.models import Address, PhoneNumber, SportOrganization


class SportType(models.Model):
    """Модель вида спорта."""
    title = models.CharField(
        verbose_name='Название вида спорта',
        max_length=255,
        blank=False
    )

    class Meta:
        verbose_name = "Вид спорта"
        verbose_name_plural = "Виды спорта"

    def __str__(self):
        return self.title


class AgeGroup(models.Model):
    """Модель возрастной группы."""
    year_from = models.PositiveIntegerField(
        verbose_name='Нижняя граница возрастной группы',
        validators=[
            MinValueValidator(1, message='Минимальное значение 1'),
            MaxValueValidator(99, message='Максимальное значение 99'),
        ],
        blank=False
    )
    year_until = models.PositiveIntegerField(
        verbose_name='Верхняя граница возрастной группы',
        validators=[
            MinValueValidator(1, message='Минимальное значение 1'),
            MaxValueValidator(99, message='Максимальное значение 99'),
        ],
        blank=False
    )

    class Meta:
        verbose_name = "Возрастная группа"
        verbose_name_plural = "Возрастные группы"

    def __str__(self):
        return f'С {self.year_from} до {self.year_until} лет'


class Section(models.Model):
    """Модель секции спортшколы."""
    sport_organization = models.ForeignKey(
        SportOrganization,
        verbose_name='Спортивная школа',
        on_delete=models.CASCADE,
        blank=False
    )
    title = models.CharField(
        verbose_name='Название секции',
        max_length=255,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    gender = models.CharField(
        verbose_name='Пол детей',
        max_length=7,
        choices=settings.GENDER_CHOICES,
        blank=True
    )
    sport_type = models.ForeignKey(
        SportType,
        verbose_name='Вид спорта',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    age_group = models.ForeignKey(
        AgeGroup,
        verbose_name='Возрастная группа',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес секции',
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    aviable = models.PositiveIntegerField(
        verbose_name='Наличие свободных мест',
        validators=[
            MaxValueValidator(999, message='Максимальное значение 999'),
        ],
        null=True,
        blank=False,
        default=0
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость посещения секции в месяц в рублях',
        validators=[
            MaxValueValidator(99999, message='Максимальное значение 99999'),
        ],
        null=True,
        blank=False,
        default=0
    )
    free_class = models.BooleanField(
        verbose_name='Бесплатное пробное занятие',
        default=False,
        blank=True
    )

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'
        ordering = ('sport_organization', 'title', )

    def __str__(self):
        return self.title


class DayOfWeek(models.Model):
    """Модель дня недели."""
    title = models.CharField(
        verbose_name='День недели',
        max_length=11,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'

    def __str__(self):
        return self.title


class Schedule(models.Model):
    """Модель расписания секции."""
    section = models.ForeignKey(
        Section,
        verbose_name='Секция',
        on_delete=models.CASCADE,
        blank=False
    )
    day = models.ManyToManyField(
        DayOfWeek,
        verbose_name='День недели',
        blank=False
    )
    time_from = models.TimeField(
        verbose_name='Время начала',
        blank=False
    )
    time_until = models.TimeField(
        verbose_name='Время окончания',
        blank=False
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return f'{self.section.title}'


class PhoneOfSection(models.Model):
    """Модель, которая связывает номер телефона и секцию спортшколы."""
    phone = models.ForeignKey(
        PhoneNumber,
        verbose_name='Номер телефона',
        on_delete=models.CASCADE,
        blank=False
    )
    section = models.ForeignKey(
        Section,
        verbose_name='Секция спортивной школы',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Телефон секции'
        verbose_name_plural = 'Телефоны секции'

    def __str__(self):
        return self.phone.value


class PhotoOfSection(models.Model):
    """Модель фотографии секции."""
    photo = models.ImageField(
        verbose_name='Фотография секции',
        upload_to='img/sections',
        blank=True
    )
    section = models.ForeignKey(
        Section,
        verbose_name='Секция',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Фотография секции'
        verbose_name_plural = 'Фотографии секции'

    def __str__(self):
        return f'Фото секции {self.section.title}'
