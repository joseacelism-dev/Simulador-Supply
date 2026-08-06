from django.contrib import admin

from .models import Indicator


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "result", "unit", "target", "traffic_light", "created_at")
    list_filter = ("company", "traffic_light", "status")
    search_fields = ("name", "code", "company__name")

