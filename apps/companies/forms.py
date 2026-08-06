from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            "name",
            "company_type",
            "country",
            "city",
            "currency",
            "target_market",
            "plants_count",
            "warehouses_count",
            "distribution_centers_count",
            "initial_capacity",
            "initial_capital",
            "difficulty",
        )
        labels = {
            "name": "Nombre de la empresa",
            "company_type": "Tipo de empresa",
            "country": "Pais",
            "city": "Ciudad",
            "currency": "Moneda",
            "target_market": "Mercado objetivo",
            "plants_count": "Numero de plantas",
            "warehouses_count": "Numero de almacenes",
            "distribution_centers_count": "Centros de distribucion",
            "initial_capacity": "Capacidad inicial",
            "initial_capital": "Capital inicial",
            "difficulty": "Nivel de dificultad",
        }

