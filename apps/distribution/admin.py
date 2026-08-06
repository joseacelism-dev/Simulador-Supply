from django.contrib import admin

from .models import Carrier, Route, Shipment, Vehicle


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "service_level", "cost_per_km", "risk_level")
    list_filter = ("company", "risk_level")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("plate", "carrier", "weight_capacity", "volume_capacity")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "origin_city", "destination_city", "distance_km", "estimated_days")
    list_filter = ("company",)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("code", "company", "order", "carrier", "status", "shipping_cost")
    list_filter = ("company", "status")

