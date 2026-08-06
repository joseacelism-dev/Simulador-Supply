from django.contrib import admin

from .models import FinishedGoodsStock, Warehouse, WarehouseLocation


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "city", "capacity_units", "is_distribution_center")
    list_filter = ("company", "is_distribution_center")


@admin.register(WarehouseLocation)
class WarehouseLocationAdmin(admin.ModelAdmin):
    list_display = ("code", "warehouse", "zone", "capacity_units")
    list_filter = ("warehouse__company",)


@admin.register(FinishedGoodsStock)
class FinishedGoodsStockAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity_available", "quantity_committed")
    list_filter = ("warehouse__company",)

