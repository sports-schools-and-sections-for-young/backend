from django.contrib import admin

from .models import (Age_group, Day_of_week, Phone_of_section,
                     Photo_of_section, Section, Section_and_Trainer, Shedule,
                     Sport_type, Trainer)


@admin.register(Sport_type)
class Sport_typeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(Age_group)
class Age_groupAdmin(admin.ModelAdmin):
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


@admin.register(Section_and_Trainer)
class Section_and_TrainerAdmin(admin.ModelAdmin):
    list_display = ('section', 'trainer')
    list_filter = ('section', 'trainer')


@admin.register(Day_of_week)
class Day_of_weekAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )


@admin.register(Shedule)
class SheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'day', 'time_from', 'time_until')
    list_filter = ('section', 'day', 'time_from', 'time_until')


@admin.register(Phone_of_section)
class Phone_of_sectionAdmin(admin.ModelAdmin):
    list_display = ('phone', 'section')
    list_filter = ('phone', 'section')


@admin.register(Photo_of_section)
class Photo_of_sectionAdmin(admin.ModelAdmin):
    list_display = ('photo', 'section')
    list_filter = ('section', )
    empty_value_display = '-пусто-'
