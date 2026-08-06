from django.contrib import admin

from .models import DispositionDecision, ReturnInspection, ReturnLine, ReturnRequest


class ReturnLineInline(admin.TabularInline):
    model = ReturnLine
    extra = 0


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "order", "reason", "status", "requested_at")
    list_filter = ("company", "status")
    search_fields = ("code", "reason", "order__code")
    inlines = [ReturnLineInline]


@admin.register(ReturnInspection)
class ReturnInspectionAdmin(admin.ModelAdmin):
    list_display = ("return_request", "accepted_quantity", "rejected_quantity", "created_at")


@admin.register(DispositionDecision)
class DispositionDecisionAdmin(admin.ModelAdmin):
    list_display = ("return_request", "decision", "recovered_value", "created_at")
    list_filter = ("decision",)

