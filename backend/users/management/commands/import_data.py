from csv import reader

from django.core.management.base import BaseCommand
from sections.models import DayOfWeek, SportType


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в БД.'

    def handle(self, *args, **options):
        try:
            with open('./data/day_of_week.csv', 'r', encoding='utf8') as file:
                file_reader = reader(file)
                for row in file_reader:
                    DayOfWeek.objects.get_or_create(title=row[0])
            with open('./data/sport_types.csv', 'r', encoding='utf8') as file:
                file_reader = reader(file)
                for row in file_reader:
                    if not SportType.objects.filter(title=row[0]).exists():
                        SportType.objects.create(
                            title=row[0],
                            moderation=True
                        )
            self.stdout.write(self.style.SUCCESS(
                'Данные успешно загружены в БД.')
            )
        except Exception as error:
            raise Exception('Ошибка при импорте данных:', error)
