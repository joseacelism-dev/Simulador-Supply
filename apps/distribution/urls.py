from django.urls import path

from .views import (
    CarrierCreateView,
    CarrierListView,
    DeliverShipmentView,
    RouteCreateView,
    RouteListView,
    ShipmentCreateView,
    ShipmentDetailView,
    ShipmentListView,
)


app_name = "distribution"

urlpatterns = [
    path("transportadores/", CarrierListView.as_view(), name="carrier_list"),
    path("empresa/<int:company_pk>/transportadores/crear/", CarrierCreateView.as_view(), name="carrier_create_for_company"),
    path("rutas/", RouteListView.as_view(), name="route_list"),
    path("empresa/<int:company_pk>/rutas/crear/", RouteCreateView.as_view(), name="route_create_for_company"),
    path("despachos/", ShipmentListView.as_view(), name="shipment_list"),
    path("empresa/<int:company_pk>/despachos/crear/", ShipmentCreateView.as_view(), name="shipment_create_for_company"),
    path("despachos/<int:pk>/", ShipmentDetailView.as_view(), name="shipment_detail"),
    path("despachos/<int:pk>/entregar/", DeliverShipmentView.as_view(), name="shipment_deliver"),
]

