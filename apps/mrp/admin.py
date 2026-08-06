from django.contrib import admin

from .models import MRPLine, MRPPlan


class MRPLineInline(admin.TabularInline):
    model = MRPLine
    extra = 0


@admin.register(MRPPlan)
class MRPPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "product", "gross_demand", "created_at")
    list_filter = ("company",)
    search_fields = ("name", "product__name", "company__name")
    inlines = [MRPLineInline]

