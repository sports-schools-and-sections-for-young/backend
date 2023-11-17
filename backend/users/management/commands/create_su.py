import os

from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Создание суперпользователя.'

    def handle(self, *args, **options):
        try:
            SU_NAME = os.getenv('SU_NAME', 'admin')
            SU_EMAIL = os.getenv('SU_EMAIL', 'admin@mail.ru')
            SU_PASSWORD = os.getenv('SU_PASSWORD', 'pass')
            if CustomUser.objects.filter(username=SU_NAME).exists():
                self.stdout.write(self.style.WARNING(
                    f'Пользователь с логином {SU_NAME} уже существует.')
                )
                return
            superuser = CustomUser.objects.create_superuser(
                username=SU_NAME,
                email=SU_EMAIL,
                password=SU_PASSWORD,
                first_name='none',
                last_name='none',
                is_active=True,
                is_staff=True
            )
            superuser.save()
            self.stdout.write(self.style.SUCCESS(
                f'Суперпользователь успешно создан (логин - {SU_NAME}, '
                f'email - {SU_EMAIL}, пароль - {SU_PASSWORD}).'
            )
            )
        except Exception as error:
            raise Exception('Ошибка при создании суперпользователя:', error)
