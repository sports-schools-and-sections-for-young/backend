from django.core.validators import MinLengthValidator
from django.db import models
from users.models import CustomUser


class SportOrganization(models.Model):
    """Модель спортшколы. """
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        blank=False
    )
    title = models.CharField(
        verbose_name='Название спортивной школы',
        max_length=255,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        unique=True,
        blank=False
    )
    address = models.CharField(
        verbose_name='Адрес спортивной школы',
        max_length=350,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
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
    phone = models.CharField(
        verbose_name='Телефон спортивной школы',
        max_length=18,
        validators=[
            MinLengthValidator(14, message='Минимум 14 символов'),
        ],
        blank=False
    )

    class Meta:
        verbose_name = 'Спортивная школа'
        verbose_name_plural = 'Спортивные школы'

    def __str__(self):
        return self.title
