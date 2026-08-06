from django.contrib import admin

from .models import InventoryItem, InventoryMovement, InventoryPolicy


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("raw_material", "company", "quantity_available", "quantity_committed", "quantity_in_transit")
    search_fields = ("raw_material__name", "raw_material__sku", "company__name")
    list_filter = ("company",)


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ("inventory_item", "movement_type", "quantity", "unit_cost", "reference", "created_at")
    search_fields = ("inventory_item__raw_material__name", "reference")
    list_filter = ("movement_type",)


@admin.register(InventoryPolicy)
class InventoryPolicyAdmin(admin.ModelAdmin):
    list_display = ("raw_material", "company", "annual_demand", "safety_stock", "lead_time_days")
    search_fields = ("raw_material__name", "company__name")
    list_filter = ("company",)

