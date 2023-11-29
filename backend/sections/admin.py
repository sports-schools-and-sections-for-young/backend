from django.conf import settings
from django.contrib import admin

from .models import (DayOfWeek, PhoneOfSection, PhotoOfSection, Schedule,
                     Section, SportType)
from .utils import DayOfWeekFilter


@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('sport_organization', 'title', 'gender', 'sport_type',
                    'year_from', 'year_until', 'address', 'aviable', 'price',
                    'free_class')
    list_filter = ('sport_organization', 'title', 'gender', 'sport_type',
                   'year_from', 'year_until', 'address', 'aviable', 'price',
                   'free_class')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'get_days', 'time_from', 'time_until')
    list_filter = ('section', DayOfWeekFilter)

    # Отображение дней недели секции в админке
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
    empty_value_display = settings.EMPTY_VALUE
