from django.conf import settings
from django.contrib import admin

from .models import (Address, PhoneNumber, PhoneOfOrganization,
                     SportOrganization)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('index', 'city', 'metro', 'district',
                    'street', 'house', 'latitude', 'longitude')
    list_filter = ('index', 'city', 'metro', 'district',
                   'street', 'house', 'latitude', 'longitude')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(SportOrganization)
class SportOrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'email', 'site', 'description')
    list_filter = ('title', 'address', 'email', 'site')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('value', 'comment')
    list_filter = ('value', )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(PhoneOfOrganization)
class PhoneOfOrganizationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'sport_school')
    list_filter = ('phone', 'sport_school')
