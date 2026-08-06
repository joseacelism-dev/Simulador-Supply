from django import forms

from .models import SustainabilityRecord


class SustainabilityRecordForm(forms.ModelForm):
    class Meta:
        model = SustainabilityRecord
        fields = (
            "period_label",
            "energy_kwh",
            "water_m3",
            "waste_kg",
            "recovered_waste_kg",
            "transport_emissions_kg",
            "recycled_material_percentage",
        )
        labels = {
            "period_label": "Periodo",
            "energy_kwh": "Energia kWh",
            "water_m3": "Agua m3",
            "waste_kg": "Residuos kg",
            "recovered_waste_kg": "Residuos recuperados kg",
            "transport_emissions_kg": "Emisiones transporte kg CO2e",
            "recycled_material_percentage": "Material reciclado porcentual",
        }

    def clean(self):
        cleaned = super().clean()
        for field in (
            "energy_kwh",
            "water_m3",
            "waste_kg",
            "recovered_waste_kg",
            "transport_emissions_kg",
            "recycled_material_percentage",
        ):
            value = cleaned.get(field)
            if value is not None and value < 0:
                self.add_error(field, "El valor no puede ser negativo.")
        return cleaned

