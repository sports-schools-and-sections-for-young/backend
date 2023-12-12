import uuid

from django.contrib.auth.models import AbstractUser
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
    password = models.CharField(max_length=10)
    username = models.CharField(max_length=12, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()
