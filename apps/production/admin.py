from django.contrib import admin

from .models import BillOfMaterials, BillOfMaterialsLine, Machine, ProductionOrder, WorkCenter


class BillOfMaterialsLineInline(admin.TabularInline):
    model = BillOfMaterialsLine
    extra = 0


@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(admin.ModelAdmin):
    list_display = ("product", "company", "version", "is_active")
    list_filter = ("company", "is_active")
    search_fields = ("product__name", "company__name")
    inlines = [BillOfMaterialsLineInline]


@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "daily_capacity", "labor_cost_per_hour")
    list_filter = ("company",)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "work_center", "hourly_capacity", "is_available")
    list_filter = ("is_available", "work_center__company")


@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "bom", "quantity", "status", "estimated_cost")
    list_filter = ("company", "status", "strategy")
    search_fields = ("code", "bom__product__name", "company__name")

