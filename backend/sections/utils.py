from django.contrib import admin

from .models import DayOfWeek


class DayOfWeekFilter(admin.SimpleListFilter):
    """Поиск в админке по дням недели секции."""
    title = 'День недели'
    parameter_name = 'day'

    def lookups(self, request, model_admin):
        return [
            (day.id, day.title) for day in DayOfWeek.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(day__id=self.value())
        return queryset
