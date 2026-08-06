from django.urls import path

from .views import SupplierCreateView


app_name = "suppliers"

urlpatterns = [
    path("empresa/<int:company_pk>/crear/", SupplierCreateView.as_view(), name="create"),
]

