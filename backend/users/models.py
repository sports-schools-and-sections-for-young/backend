from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель кастомного пользователя.
    Переопределил поле username, чтобы сделать свою валидацию и для
    отображения понятного названия поля.
    """
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=60,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов'),
            RegexValidator(
                regex=r'^[a-z0-9]+$',
                message='Логин может содержать только символы '
                        'английского алфавита и цифры.'
            ),
        ],
        unique=True,
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_email_username'
            )
        ]

    def __str__(self):
        return self.get_full_name()
