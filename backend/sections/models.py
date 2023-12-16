from django.conf import settings
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from organizations.models import SportOrganization


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
        ordering = ('title', )

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
        blank=False,
        null=True
    )
    schedule = models.ManyToManyField(
        DayOfWeek,
        verbose_name='День недели',
        blank=False
    )
    year_from = models.PositiveIntegerField(
        verbose_name='Нижняя граница возрастной группы',
        validators=[
            MinValueValidator(3, message='Минимальное значение 3'),
            MaxValueValidator(18, message='Максимальное значение 18'),
        ],
        blank=False
    )
    year_until = models.PositiveIntegerField(
        verbose_name='Верхняя граница возрастной группы',
        validators=[
            MinValueValidator(3, message='Минимальное значение 3'),
            MaxValueValidator(18, message='Максимальное значение 18'),
        ],
        blank=False
    )
    address = models.CharField(
        verbose_name='Адрес секции',
        max_length=350,
        blank=False
    )
    latitude = models.DecimalField(
        verbose_name='Широта',
        max_digits=12,
        decimal_places=6,
        blank=False,
        null=True,
        default=0
    )
    longitude = models.DecimalField(
        verbose_name='Долгота',
        max_digits=12,
        decimal_places=6,
        blank=False,
        null=True,
        default=0
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость посещения секции в месяц в рублях',
        validators=[
            MaxValueValidator(99999, message='Максимальное значение 99999'),
        ],
        blank=False,
        null=True,
        default=0
    )
    free_class = models.BooleanField(
        verbose_name='Бесплатное пробное занятие',
        blank=True,
        default=False
    )

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'
        ordering = ('sport_organization', 'title', )

    def __str__(self):
        return self.title
