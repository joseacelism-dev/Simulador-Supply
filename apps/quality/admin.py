from django.contrib import admin

from .models import CustomerComplaint, NonConformance, QualityInspection


class NonConformanceInline(admin.TabularInline):
    model = NonConformance
    extra = 0


@admin.register(QualityInspection)
class QualityInspectionAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "product", "inspected_quantity", "nonconforming_quantity", "status")
    list_filter = ("company", "status")
    search_fields = ("code", "product__name", "company__name")
    inlines = [NonConformanceInline]


@admin.register(CustomerComplaint)
class CustomerComplaintAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "product", "reason", "status")
    list_filter = ("company", "status")
    search_fields = ("code", "reason", "product__name")

