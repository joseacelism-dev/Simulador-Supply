from django.contrib import admin

from .models import CustomerOrder, CustomerOrderLine


class CustomerOrderLineInline(admin.TabularInline):
    model = CustomerOrderLine
    extra = 0


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "customer", "status", "priority", "promised_date")
    list_filter = ("company", "status")
    search_fields = ("code", "customer__name", "company__name")
    inlines = [CustomerOrderLineInline]

