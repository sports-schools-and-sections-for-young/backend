from django.contrib import admin

from .models import (Address, Order, Phone_number, Phone_of_organization,
                     Rewiev, Sport_organization)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('index', 'city', 'metro', 'district',
                    'street', 'house')
    list_filter = ('index', 'city', 'metro', 'district',
                   'street', 'house')
    empty_value_display = '-пусто-'


@admin.register(Sport_organization)
class Sport_organizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'logo', 'address', 'email',
                    'site', 'description')
    list_filter = ('title', 'logo', 'address', 'email',
                   'site')
    empty_value_display = '-пусто-'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('sport_organization', 'fio', 'age', 'gender',
                    'phone', 'comment')
    list_filter = ('sport_organization', 'fio', 'age', 'gender',
                   'phone')
    empty_value_display = '-пусто-'


@admin.register(Phone_number)
class Phone_numberAdmin(admin.ModelAdmin):
    list_display = ('value', 'comment')
    list_filter = ('value', )
    empty_value_display = '-пусто-'


@admin.register(Phone_of_organization)
class Phone_of_organizationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'sport_school')
    list_filter = ('phone', 'sport_school')


@admin.register(Rewiev)
class RewievAdmin(admin.ModelAdmin):
    list_display = ('comment', 'date_and_time', 'rating', 'sport_school')
    list_filter = ('date_and_time', 'rating', 'sport_school')
    empty_value_display = '-пусто-'
