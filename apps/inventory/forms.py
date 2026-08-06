from django import forms

from .models import InventoryPolicy


class InventoryPolicyForm(forms.ModelForm):
    class Meta:
        model = InventoryPolicy
        fields = (
            "raw_material",
            "annual_demand",
            "ordering_cost",
            "holding_cost",
            "daily_demand",
            "lead_time_days",
            "safety_stock",
        )
        labels = {
            "raw_material": "Materia prima",
            "annual_demand": "Demanda anual",
            "ordering_cost": "Costo de ordenar",
            "holding_cost": "Costo anual de mantener",
            "daily_demand": "Demanda diaria",
            "lead_time_days": "Lead time en dias",
            "safety_stock": "Stock de seguridad",
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["raw_material"].queryset = company.raw_materials.all()

    def clean(self):
        cleaned_data = super().clean()
        for field in ("annual_demand", "ordering_cost", "holding_cost", "daily_demand", "safety_stock"):
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, "El valor no puede ser negativo.")
        return cleaned_data

