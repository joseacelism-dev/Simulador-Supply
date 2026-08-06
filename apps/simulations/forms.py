from django import forms

from .models import Decision, Simulation


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ("name", "scenario", "total_periods", "periodicity")
        labels = {
            "name": "Nombre",
            "scenario": "Escenario",
            "total_periods": "Periodos totales",
            "periodicity": "Periodicidad",
        }


class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ("area", "title", "description")
        labels = {
            "area": "Area",
            "title": "Titulo",
            "description": "Descripcion",
        }

