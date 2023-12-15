from django.conf import settings
from django.contrib import admin

from .models import SportOrganization


@admin.register(SportOrganization)
class SportOrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_username', 'address', 'email', 'site')
    list_filter = ('title', 'user__username', 'address')
    empty_value_display = settings.EMPTY_VALUE

    # Отображение владельца спортшколы в админке
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Владелец'
