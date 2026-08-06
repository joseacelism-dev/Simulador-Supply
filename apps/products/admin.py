from django.contrib import admin

from .models import Product, RawMaterial


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "company", "unit", "sale_price")
    search_fields = ("sku", "name", "company__name")
    list_filter = ("company",)


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "company", "unit", "standard_cost", "is_perishable")
    search_fields = ("sku", "name", "company__name")
    list_filter = ("company", "is_perishable")

