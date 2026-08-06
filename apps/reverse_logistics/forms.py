from django import forms

from .models import DispositionDecision, ReturnInspection, ReturnLine, ReturnRequest


class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ("code", "order", "reason")
        labels = {"code": "Codigo", "order": "Pedido", "reason": "Motivo"}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["order"].queryset = company.customer_orders.all()


class ReturnLineForm(forms.ModelForm):
    class Meta:
        model = ReturnLine
        fields = ("product", "quantity", "condition")
        labels = {"product": "Producto", "quantity": "Cantidad", "condition": "Estado del producto"}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["product"].queryset = company.products.all()

    def clean_quantity(self):
        value = self.cleaned_data["quantity"]
        if value <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return value


class ReturnInspectionForm(forms.ModelForm):
    class Meta:
        model = ReturnInspection
        fields = ("accepted_quantity", "rejected_quantity", "notes")
        labels = {
            "accepted_quantity": "Cantidad aceptada",
            "rejected_quantity": "Cantidad rechazada",
            "notes": "Notas",
        }


class DispositionDecisionForm(forms.ModelForm):
    class Meta:
        model = DispositionDecision
        fields = ("decision", "recovered_value", "environmental_impact", "notes")
        labels = {
            "decision": "Decision",
            "recovered_value": "Valor recuperado",
            "environmental_impact": "Impacto ambiental",
            "notes": "Notas",
        }

    def clean_recovered_value(self):
        value = self.cleaned_data["recovered_value"]
        if value < 0:
            raise forms.ValidationError("El valor recuperado no puede ser negativo.")
        return value

