from django import forms

from .models import CustomerComplaint, NonConformance, QualityInspection


class QualityInspectionForm(forms.ModelForm):
    class Meta:
        model = QualityInspection
        fields = ("code", "product", "inspected_quantity", "conforming_quantity", "nonconforming_quantity", "notes")
        labels = {
            "code": "Codigo",
            "product": "Producto",
            "inspected_quantity": "Cantidad inspeccionada",
            "conforming_quantity": "Cantidad conforme",
            "nonconforming_quantity": "Cantidad no conforme",
            "notes": "Notas",
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["product"].queryset = company.products.all()

    def clean(self):
        cleaned = super().clean()
        inspected = cleaned.get("inspected_quantity")
        conforming = cleaned.get("conforming_quantity")
        nonconforming = cleaned.get("nonconforming_quantity")
        if inspected is not None and inspected <= 0:
            self.add_error("inspected_quantity", "La cantidad inspeccionada debe ser mayor que cero.")
        if conforming is not None and conforming < 0:
            self.add_error("conforming_quantity", "La cantidad no puede ser negativa.")
        if nonconforming is not None and nonconforming < 0:
            self.add_error("nonconforming_quantity", "La cantidad no puede ser negativa.")
        if inspected is not None and conforming is not None and nonconforming is not None:
            if conforming + nonconforming > inspected:
                self.add_error("nonconforming_quantity", "Las cantidades no pueden superar la cantidad inspeccionada.")
        return cleaned


class NonConformanceForm(forms.ModelForm):
    class Meta:
        model = NonConformance
        fields = ("defect_type", "quantity", "root_cause", "corrective_action")
        labels = {
            "defect_type": "Tipo de defecto",
            "quantity": "Cantidad",
            "root_cause": "Causa raiz",
            "corrective_action": "Accion correctiva",
        }


class CustomerComplaintForm(forms.ModelForm):
    class Meta:
        model = CustomerComplaint
        fields = ("code", "order", "product", "reason", "description")
        labels = {"code": "Codigo", "order": "Pedido", "product": "Producto", "reason": "Motivo", "description": "Descripcion"}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["order"].queryset = company.customer_orders.all()
            self.fields["product"].queryset = company.products.all()

