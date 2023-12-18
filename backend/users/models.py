from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель кастомного пользователя."""
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
        validators=[
            MinLengthValidator(8, message='Минимум 8 символов')
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()
