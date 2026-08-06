from django.urls import path

from .views import (
    PurchaseOrderCreateView,
    PurchaseOrderDetailView,
    PurchaseOrderListView,
    ReceivePurchaseOrderView,
)


app_name = "purchasing"

urlpatterns = [
    path("", PurchaseOrderListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/crear/", PurchaseOrderCreateView.as_view(), name="create_for_company"),
    path("<int:pk>/", PurchaseOrderDetailView.as_view(), name="detail"),
    path("<int:pk>/recibir/", ReceivePurchaseOrderView.as_view(), name="receive"),
]

