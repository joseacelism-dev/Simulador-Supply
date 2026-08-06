from django.urls import path

from .views import FinishedGoodsStockCreateView, FinishedGoodsStockListView, WarehouseCreateView, WarehouseListView


app_name = "warehouses"

urlpatterns = [
    path("", WarehouseListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/crear/", WarehouseCreateView.as_view(), name="create_for_company"),
    path("stock/", FinishedGoodsStockListView.as_view(), name="stock_list"),
    path("empresa/<int:company_pk>/stock/crear/", FinishedGoodsStockCreateView.as_view(), name="stock_create_for_company"),
]

