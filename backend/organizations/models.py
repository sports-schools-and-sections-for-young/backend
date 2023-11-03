from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinLengthValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class Address(models.Model):
    """Модель адреса секции или спортшколы."""
    index = models.PositiveIntegerField(
        verbose_name='Индекс',
        validators=[
            MinLengthValidator(6, message='Минимум 6 символов'),
            MaxLengthValidator(6, message='Максимум 6 символов')
        ],
        blank=False
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=25,
        validators=[
            MinLengthValidator(2, message='Минимум 2 символа')
        ],
        blank=False
    )
    metro = models.CharField(
        verbose_name='Метро',
        max_length=65,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=True
    )
    district = models.CharField(
        verbose_name='Район',
        max_length=65,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=150,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    house = models.PositiveIntegerField(
        verbose_name='Дом',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(6, message='Максимум 65 символов')
        ],
        blank=False
    )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ('city', 'street', 'house', )

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}'


class SportOrganization(models.Model):
    """Модель спортшколы."""
    title = models.CharField(
        verbose_name='Название организации',
        max_length=255,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    logo = models.ImageField(
        verbose_name='Логотип организации',
        upload_to='img/organizations',
        blank=False
    )
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес спортивной школы',
        on_delete=models.CASCADE,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=320,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        unique=True,
        blank=False
    )
    site = models.CharField(
        verbose_name='Сайт или страничка в VK',
        max_length=255,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание организации',
        max_length=20000,
        blank=False
    )
    login = models.CharField(
        verbose_name='Логин',
        max_length=60,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов'),
            RegexValidator(
                regex=r'^[a-z]+$',
                message='Логин может содержать только символы '
                        'английского алфавита.'
            ),
        ],
        unique=True,
        blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=16,
        validators=[
            MinLengthValidator(8, message='Минимум 8 символов'),
        ],
        blank=False
    )

    class Meta:
        verbose_name = 'Спортивная школа'
        verbose_name_plural = 'Спортивные школы'
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'login'),
                name='unique_email_login'
            )
        ]

    def __str__(self):
        return self.title


class Order(models.Model):
    """Модель заявки."""
    sport_organization = models.ForeignKey(
        SportOrganization,
        verbose_name='Спортивная школа',
        on_delete=models.CASCADE,
        blank=False
    )
    fio = models.CharField(
        verbose_name='Фамилия Имя Отчество',
        max_length=255,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    age = models.PositiveIntegerField(
        verbose_name='Возраст ребенка',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(6, message='Максимум 2 символа')
        ],
        blank=False
    )
    gender = models.CharField(
        verbose_name='Пол ребенка',
        max_length=7,
        blank=False
    )
    phone = models.CharField(
        verbose_name='Номер телефона для связи',
        max_length=18,
        validators=[
            MinLengthValidator(18, message='Минимум 18 символов'),
            RegexValidator(
                regex=r'^\+7\(\d{3}\)\d{7}$',
                message='Неправильный формат номера телефона.'
            ),
        ],
        blank=False
    )
    comment = models.CharField(
        verbose_name='Комментраий к заявке',
        max_length=255,
        blank=True
    )


class PhoneNumber(models.Model):
    """Модель номера телефона."""
    value = models.CharField(
        verbose_name='Номер телефона',
        max_length=18,
        validators=[
            MinLengthValidator(18, message='Минимум 18 символов'),
            RegexValidator(
                regex=r'^\+7\(\d{3}\)\d{7}$',
                message='Неправильный формат номера телефона.'
            ),
        ],
        blank=False
    )
    comment = models.CharField(
        verbose_name='Комментарий к номеру телефона',
        max_length=30,
        blank=True
    )


class PhoneOfOrganization(models.Model):
    """Модель, которая связывает номера телефона и спортшколу."""
    phone = models.ForeignKey(
        PhoneNumber,
        verbose_name='Телефон',
        on_delete=models.CASCADE,
        blank=False
    )
    sport_school = models.ForeignKey(
        SportOrganization,
        verbose_name='Спортивная школа',
        on_delete=models.CASCADE,
        blank=False
    )


class Rewiev(models.Model):
    """Модель отзыва о спортшколе."""
    comment = models.CharField(
        verbose_name='Текст отзыва',
        max_length=255,
        blank=True
    )
    date_and_time = models.DateTimeField(
        verbose_name='Дата и время оставления отзыва',
        auto_now_add=True,
        blank=False
    )
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(1, message='Максимум 1 символ'),
            MinValueValidator(1, message='Минимумальное значение 1'),
            MaxValueValidator(5, message='Максимальное значение 5'),
        ],
        blank=False
    )
    sport_school = models.ForeignKey(
        SportOrganization,
        verbose_name='Спортивная школа',
        on_delete=models.CASCADE,
        blank=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('id', )
