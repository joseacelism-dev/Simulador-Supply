from django import forms

from .models import Carrier, Route, Shipment


class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = ("name", "service_level", "cost_per_km", "risk_level")
        labels = {
            "name": "Nombre",
            "service_level": "Nivel de servicio",
            "cost_per_km": "Costo por km",
            "risk_level": "Nivel de riesgo",
        }


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("name", "origin_city", "destination_city", "distance_km", "estimated_days", "risk_level")
        labels = {
            "name": "Nombre",
            "origin_city": "Ciudad origen",
            "destination_city": "Ciudad destino",
            "distance_km": "Distancia km",
            "estimated_days": "Dias estimados",
            "risk_level": "Nivel de riesgo",
        }


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ("code", "order", "warehouse", "carrier", "route")
        labels = {
            "code": "Codigo",
            "order": "Pedido",
            "warehouse": "Almacen",
            "carrier": "Transportador",
            "route": "Ruta",
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["order"].queryset = company.customer_orders.exclude(
                status__in=["despachado", "entregado", "cancelado"]
            )
            self.fields["warehouse"].queryset = company.warehouses.all()
            self.fields["carrier"].queryset = company.carriers.all()
            self.fields["route"].queryset = company.routes.all()

