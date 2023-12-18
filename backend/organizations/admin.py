from django.conf import settings
from django.contrib import admin

from .models import SportOrganization


@admin.register(SportOrganization)
class SportOrganizationAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_username', 'address', 'email', 'site')
    list_filter = ('title', 'user__username', 'address')
    empty_value_display = settings.EMPTY_VALUE

    # Отображение владельца спортшколы в админке
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Владелец'

    # Сокращенное отображение title в админке
    def get_title(self, obj):
        return str(obj.title)[:50]
    get_title.short_description = 'Название спортивной школы'
