from django import forms

from .models import MRPPlan


class MRPPlanForm(forms.ModelForm):
    class Meta:
        model = MRPPlan
        fields = ("name", "product", "gross_demand", "planned_receipt_date")
        labels = {
            "name": "Nombre",
            "product": "Producto",
            "gross_demand": "Demanda bruta",
            "planned_receipt_date": "Fecha de recepcion planificada",
        }
        widgets = {"planned_receipt_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["product"].queryset = company.products.all()

    def clean_gross_demand(self):
        value = self.cleaned_data["gross_demand"]
        if value <= 0:
            raise forms.ValidationError("La demanda bruta debe ser mayor que cero.")
        return value

