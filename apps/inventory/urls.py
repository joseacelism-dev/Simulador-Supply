from django.urls import path

from .views import InventoryListView, InventoryPolicyCreateView, InventoryPolicyListView


app_name = "inventory"

urlpatterns = [
    path("", InventoryListView.as_view(), name="list"),
    path("politicas/", InventoryPolicyListView.as_view(), name="policy_list"),
    path("empresa/<int:company_pk>/politicas/crear/", InventoryPolicyCreateView.as_view(), name="policy_create_for_company"),
]

