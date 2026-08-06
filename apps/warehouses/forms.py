from django import forms

from .models import FinishedGoodsStock, Warehouse, WarehouseLocation


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ("name", "city", "capacity_units", "is_distribution_center")
        labels = {
            "name": "Nombre",
            "city": "Ciudad",
            "capacity_units": "Capacidad en unidades",
            "is_distribution_center": "Centro de distribucion",
        }


class WarehouseLocationForm(forms.ModelForm):
    class Meta:
        model = WarehouseLocation
        fields = ("code", "zone", "capacity_units")
        labels = {"code": "Codigo", "zone": "Zona", "capacity_units": "Capacidad en unidades"}


class FinishedGoodsStockForm(forms.ModelForm):
    class Meta:
        model = FinishedGoodsStock
        fields = ("warehouse", "product", "quantity_available")
        labels = {"warehouse": "Almacen", "product": "Producto", "quantity_available": "Cantidad disponible"}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["warehouse"].queryset = company.warehouses.all()
            self.fields["product"].queryset = company.products.all()

    def clean_quantity_available(self):
        value = self.cleaned_data["quantity_available"]
        if value < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return value

