from django.contrib import admin

from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderLineInline(admin.TabularInline):
    model = PurchaseOrderLine
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "supplier", "status", "order_date", "expected_receipt_date")
    search_fields = ("code", "company__name", "supplier__name")
    list_filter = ("status", "company")
    inlines = [PurchaseOrderLineInline]

