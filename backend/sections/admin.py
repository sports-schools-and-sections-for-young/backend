from django.conf import settings
from django.contrib import admin

from .models import DayOfWeek, Section, SportType
from .utils import ScheduleFilter


@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'moderation')
    list_filter = ('title', 'moderation')
    list_editable = ('moderation', )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('get_sport_organization', 'title', 'gender', 'sport_type',
                    'get_schedule', 'year_from', 'year_until', 'address',
                    'price', 'free_class', 'moderation')
    list_filter = ('sport_organization', 'title', 'gender', 'sport_type',
                   ScheduleFilter, 'year_from', 'year_until', 'address',
                   'price', 'free_class', 'moderation')
    list_editable = ('moderation', )
    empty_value_display = settings.EMPTY_VALUE

    # Отображение дней работы секции в админке
    def get_schedule(self, obj):
        return ", ".join([day.title for day in obj.schedule.all()])
    get_schedule.short_description = 'Расписание'

    # Сокращенное отображение sport_organization в админке
    def get_sport_organization(self, obj):
        return str(obj.sport_organization)[:50]
    get_sport_organization.short_description = 'Спортивная школа'


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )
