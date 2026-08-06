from django.urls import path

from .views import (
    BillOfMaterialsCreateView,
    BillOfMaterialsDetailView,
    BillOfMaterialsListView,
    CompleteProductionOrderView,
    ProductionOrderCreateView,
    ProductionOrderDetailView,
    ProductionOrderListView,
)


app_name = "production"

urlpatterns = [
    path("bom/", BillOfMaterialsListView.as_view(), name="bom_list"),
    path("bom/empresa/<int:company_pk>/crear/", BillOfMaterialsCreateView.as_view(), name="bom_create_for_company"),
    path("bom/<int:pk>/", BillOfMaterialsDetailView.as_view(), name="bom_detail"),
    path("ordenes/", ProductionOrderListView.as_view(), name="order_list"),
    path("ordenes/empresa/<int:company_pk>/crear/", ProductionOrderCreateView.as_view(), name="order_create_for_company"),
    path("ordenes/<int:pk>/", ProductionOrderDetailView.as_view(), name="order_detail"),
    path("ordenes/<int:pk>/completar/", CompleteProductionOrderView.as_view(), name="order_complete"),
]

