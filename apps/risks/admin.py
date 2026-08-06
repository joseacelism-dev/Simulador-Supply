from django.contrib import admin

from .models import RiskEvent, RiskResponse


class RiskResponseInline(admin.TabularInline):
    model = RiskResponse
    extra = 0


@admin.register(RiskEvent)
class RiskEventAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "category", "probability", "impact", "exposure_score", "status")
    list_filter = ("company", "category", "status")
    search_fields = ("title", "description", "company__name")
    inlines = [RiskResponseInline]

