from django.urls import path

from .views import ProductCreateView, RawMaterialCreateView


app_name = "products"

urlpatterns = [
    path("empresa/<int:company_pk>/crear/", ProductCreateView.as_view(), name="create"),
    path("empresa/<int:company_pk>/materias-primas/crear/", RawMaterialCreateView.as_view(), name="raw_material_create"),
]

