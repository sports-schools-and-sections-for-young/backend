from django.contrib import admin

from .models import (AgeGroup, DayOfWeek, PhoneOfSection, PhotoOfSection,
                     Section, SectionTrainer, Shedule, SportType, Trainer)
from .utils import DayOfWeekFilter


@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ('year_from', 'year_until')
    list_filter = ('year_from', 'year_until')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('sport_organization', 'title', 'gender', 'sport_type',
                    'age_group', 'address', 'aviable', 'price')
    list_filter = ('sport_organization', 'title', 'gender', 'sport_type',
                   'age_group', 'address', 'aviable', 'price')
    empty_value_display = '-пусто-'


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('fio', 'info', 'photo')
    list_filter = ('fio', )
    empty_value_display = '-пусто-'


@admin.register(SectionTrainer)
class SectionTrainerAdmin(admin.ModelAdmin):
    list_display = ('section', 'trainer')
    list_filter = ('section', 'trainer')


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(Shedule)
class SheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'get_days', 'time_from', 'time_until')
    list_filter = ('section', DayOfWeekFilter)

    # Метод для отображения дней недели в админке
    def get_days(self, obj):
        return ", ".join([day.title for day in obj.day.all()])


@admin.register(PhoneOfSection)
class PhoneOfSectionAdmin(admin.ModelAdmin):
    list_display = ('phone', 'section')
    list_filter = ('phone', 'section')


@admin.register(PhotoOfSection)
class PhotoOfSectionAdmin(admin.ModelAdmin):
    list_display = ('section', )
    list_filter = ('section', )
    empty_value_display = '-пусто-'
