import os

from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Создание суперпользователя.'

    def handle(self, *args, **options):
        try:
            su_name = os.getenv('SU_NAME', 'admin')
            su_email = os.getenv('SU_EMAIL', 'admin@mail.ru')
            su_password = os.getenv('SU_PASSWORD', 'pass')
            if CustomUser.objects.filter(username=su_name).exists():
                self.stdout.write(self.style.WARNING(
                    f'Пользователь с логином {su_name} уже существует.')
                )
                return
            superuser = CustomUser.objects.create_superuser(
                username=su_name,
                email=su_email,
                password=su_password,
                first_name='none',
                last_name='none',
                is_active=True,
                is_staff=True
            )
            superuser.save()
            self.stdout.write(self.style.SUCCESS(
                f'Суперпользователь успешно создан (логин - {su_name}, '
                f'email - {su_email}, пароль - {su_password}).'
            )
            )
        except Exception as error:
            raise Exception('Ошибка при создании суперпользователя:', error)
