from django.db import models

from apps.companies.models import Company
from apps.simulations.models import Simulation, SimulationPeriod


class Indicator(models.Model):
    class Status(models.TextChoices):
        GOOD = "bueno", "Bueno"
        WARNING = "advertencia", "Advertencia"
        CRITICAL = "critico", "Critico"

    class TrafficLight(models.TextChoices):
        GREEN = "verde", "Verde"
        YELLOW = "amarillo", "Amarillo"
        RED = "rojo", "Rojo"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="indicators", verbose_name="empresa")
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name="indicators", verbose_name="simulacion", null=True, blank=True)
    period = models.ForeignKey(SimulationPeriod, on_delete=models.CASCADE, related_name="indicators", verbose_name="periodo", null=True, blank=True)
    code = models.CharField("codigo", max_length=80)
    name = models.CharField("nombre", max_length=160)
    formula = models.TextField("formula")
    result = models.DecimalField("resultado", max_digits=14, decimal_places=2)
    unit = models.CharField("unidad", max_length=40, blank=True)
    target = models.DecimalField("meta", max_digits=14, decimal_places=2, default=0)
    status = models.CharField("estado", max_length=30, choices=Status.choices)
    traffic_light = models.CharField("semaforo", max_length=20, choices=TrafficLight.choices)
    interpretation = models.TextField("interpretacion")
    recommendation = models.TextField("recomendacion")
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "indicador"
        verbose_name_plural = "indicadores"

    def __str__(self):
        return self.name

