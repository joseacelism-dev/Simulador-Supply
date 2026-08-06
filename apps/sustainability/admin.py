from django.contrib import admin

from .models import SustainabilityRecord


@admin.register(SustainabilityRecord)
class SustainabilityRecordAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "period_label",
        "energy_kwh",
        "water_m3",
        "waste_kg",
        "recovered_waste_kg",
        "transport_emissions_kg",
    )
    list_filter = ("company",)
    search_fields = ("company__name", "period_label")

