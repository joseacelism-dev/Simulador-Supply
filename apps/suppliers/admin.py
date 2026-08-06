from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "location", "lead_time_days", "reliability", "risk_level")
    search_fields = ("name", "company__name", "location")
    list_filter = ("company", "risk_level")

