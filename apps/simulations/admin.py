from django.contrib import admin

from .models import Decision, PeriodResult, Simulation, SimulationEvent, SimulationPeriod


class SimulationPeriodInline(admin.TabularInline):
    model = SimulationPeriod
    extra = 0


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "scenario", "status", "current_period_number", "total_periods")
    search_fields = ("name", "company__name", "company__owner__username")
    list_filter = ("status", "periodicity", "scenario")
    inlines = [SimulationPeriodInline]


@admin.register(SimulationPeriod)
class SimulationPeriodAdmin(admin.ModelAdmin):
    list_display = ("simulation", "number", "status", "opened_at", "closed_at")
    list_filter = ("status",)


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ("title", "period", "area", "locked", "created_at")
    search_fields = ("title", "description", "period__simulation__name")
    list_filter = ("area", "locked")


@admin.register(SimulationEvent)
class SimulationEventAdmin(admin.ModelAdmin):
    list_display = ("name", "period", "severity", "created_at")
    search_fields = ("name", "description", "period__simulation__name")
    list_filter = ("severity",)


@admin.register(PeriodResult)
class PeriodResultAdmin(admin.ModelAdmin):
    list_display = ("period", "available_capital", "operational_score", "decision_count")

