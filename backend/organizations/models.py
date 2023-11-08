from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator, RegexValidator)
from django.db import models

GENDER_CHOICES = (
    ('Man', 'Мужской'),
    ('Woman', 'Женский'),
)


class Address(models.Model):
    """Модель адреса секции или спортшколы."""
    index = models.PositiveIntegerField(
        verbose_name='Индекс',
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Неправильный формат индекса'
            ),
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
    house = models.CharField(
        verbose_name='Дом',
        max_length=20,
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ')
        ],
        blank=False
    )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ('city', 'street', 'house', )

    def __str__(self):
        return (f'{self.index}, {self.city}, {self.district}, {self.street}, '
                f'{self.house}')


class SportOrganization(models.Model):
    """
    Модель спортшколы.
    Алгоритм добавления спортшколы: пользователь регистрируется на сайте со
    следующими полями: логин, e-mail, имя, фамилия, пароль. Затем пользователь
    авторизуется на сайте и в личном кабинете добавляет спортшколу.
    """
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
        blank=True
    )
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес спортивной школы',
        on_delete=models.SET_NULL,
        null=True,
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
    site = models.URLField(
        verbose_name='Сайт или страничка в VK',
        max_length=255,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание организации',
        max_length=20000,
        blank=False
    )

    class Meta:
        verbose_name = 'Спортивная школа'
        verbose_name_plural = 'Спортивные школы'

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
            MinValueValidator(1, message='Минимальное значение 1'),
            MaxValueValidator(99, message='Максимальное значение 99'),
        ],
        blank=False
    )
    gender = models.CharField(
        verbose_name='Пол ребенка',
        max_length=7,
        choices=GENDER_CHOICES,
        blank=False
    )
    phone = models.CharField(
        verbose_name='Номер телефона для связи',
        max_length=18,
        validators=[
            MinLengthValidator(14, message='Минимум 14 символов'),
        ],
        blank=False
    )
    comment = models.CharField(
        verbose_name='Комментарий к заявке',
        max_length=255,
        blank=True
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка в спортшколу {self.sport_organization.title}'


class PhoneNumber(models.Model):
    """Модель номера телефона."""
    value = models.CharField(
        verbose_name='Номер телефона',
        max_length=18,
        validators=[
            MinLengthValidator(14, message='Минимум 14 символов'),
        ],
        blank=False
    )
    comment = models.CharField(
        verbose_name='Комментарий к номеру телефона',
        max_length=30,
        blank=True
    )

    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'

    def __str__(self):
        return self.value


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

    class Meta:
        verbose_name = 'Телефон спортшколы'
        verbose_name_plural = 'Телефоны спортшколы'

    def __str__(self):
        return f'Телефон спортшколы {self.sport_school}'


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
            MinValueValidator(1, message='Минимумальное значение 1'),
            MaxValueValidator(5, message='Максимальное значение 5'),
        ],
        blank=False
    )
    sport_school = models.ForeignKey(
        SportOrganization,
        verbose_name='Спортивная школа',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('id', )

    def __str__(self):
        return f'Отзыв о спортшколе {self.sport_school.title}'
