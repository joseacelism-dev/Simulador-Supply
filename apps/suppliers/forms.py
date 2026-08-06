from django import forms

from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            "name",
            "location",
            "currency",
            "lead_time_days",
            "reliability",
            "quality_score",
            "payment_terms",
            "minimum_order_quantity",
            "risk_level",
            "certifications",
        )
        labels = {
            "name": "Nombre",
            "location": "Ubicacion",
            "currency": "Moneda",
            "lead_time_days": "Lead time en dias",
            "reliability": "Confiabilidad porcentual",
            "quality_score": "Calidad porcentual",
            "payment_terms": "Condiciones de pago",
            "minimum_order_quantity": "Cantidad minima de pedido",
            "risk_level": "Nivel de riesgo",
            "certifications": "Certificaciones",
        }

