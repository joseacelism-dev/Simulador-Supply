from django import forms

from .models import RiskEvent, RiskResponse


class RiskEventForm(forms.ModelForm):
    class Meta:
        model = RiskEvent
        fields = ("category", "title", "probability", "impact", "description")
        labels = {
            "category": "Categoria",
            "title": "Titulo",
            "probability": "Probabilidad porcentual",
            "impact": "Impacto porcentual",
            "description": "Descripcion",
        }


class RiskResponseForm(forms.ModelForm):
    class Meta:
        model = RiskResponse
        fields = ("strategy", "action", "estimated_cost", "effectiveness")
        labels = {
            "strategy": "Estrategia",
            "action": "Accion",
            "estimated_cost": "Costo estimado",
            "effectiveness": "Efectividad porcentual",
        }

