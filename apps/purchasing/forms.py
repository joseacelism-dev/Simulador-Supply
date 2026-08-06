from django import forms

from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ("code", "supplier", "notes")
        labels = {
            "code": "Codigo",
            "supplier": "Proveedor",
            "notes": "Notas",
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["supplier"].queryset = company.suppliers.all()


class PurchaseOrderLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderLine
        fields = ("raw_material", "quantity", "unit_cost")
        labels = {
            "raw_material": "Materia prima",
            "quantity": "Cantidad",
            "unit_cost": "Costo unitario",
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["raw_material"].queryset = company.raw_materials.all()

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return quantity

    def clean_unit_cost(self):
        unit_cost = self.cleaned_data["unit_cost"]
        if unit_cost < 0:
            raise forms.ValidationError("El costo unitario no puede ser negativo.")
        return unit_cost

