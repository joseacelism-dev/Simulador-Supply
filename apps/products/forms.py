from django import forms

from .models import Product, RawMaterial


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("sku", "name", "description", "unit", "sale_price")
        labels = {
            "sku": "SKU",
            "name": "Nombre",
            "description": "Descripcion",
            "unit": "Unidad",
            "sale_price": "Precio de venta",
        }


class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ("sku", "name", "description", "unit", "standard_cost", "is_perishable")
        labels = {
            "sku": "SKU",
            "name": "Nombre",
            "description": "Descripcion",
            "unit": "Unidad",
            "standard_cost": "Costo estandar",
            "is_perishable": "Perecedera",
        }

