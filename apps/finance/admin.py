from django.contrib import admin

from .models import FinancialSnapshot, FinancialTransaction


@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ("description", "company", "category", "amount", "transaction_date")
    list_filter = ("company", "category")
    search_fields = ("description", "company__name")


@admin.register(FinancialSnapshot)
class FinancialSnapshotAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "total_revenue", "total_costs", "profit", "cash_flow")
    list_filter = ("company",)

