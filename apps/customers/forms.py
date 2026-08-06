from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "segment", "city", "country", "expected_service_level", "payment_terms")
        labels = {
            "name": "Nombre",
            "segment": "Segmento",
            "city": "Ciudad",
            "country": "Pais",
            "expected_service_level": "Nivel de servicio esperado",
            "payment_terms": "Condiciones de pago",
        }

