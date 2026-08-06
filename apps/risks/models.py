from django.db import models

from apps.companies.models import Company


class RiskEvent(models.Model):
    class Category(models.TextChoices):
        SUPPLIER_DELAY = "retraso_proveedor", "Retraso de proveedor"
        PRICE_INCREASE = "aumento_precios", "Aumento de precios"
        MACHINE_FAILURE = "falla_maquinaria", "Falla de maquinaria"
        TRANSPORT_BLOCK = "bloqueo_vias", "Bloqueo de vias"
        MATERIAL_SHORTAGE = "escasez_material", "Escasez de materia prima"
        DEMAND_SPIKE = "aumento_demanda", "Aumento inesperado de demanda"
        DEMAND_DROP = "caida_demanda", "Caida de demanda"
        QUALITY_PROBLEM = "problema_calidad", "Problema de calidad"
        CLIMATE = "clima", "Evento climatico"

    class Status(models.TextChoices):
        OPEN = "abierto", "Abierto"
        MITIGATED = "mitigado", "Mitigado"
        RECOVERED = "recuperado", "Recuperado"
        CLOSED = "cerrado", "Cerrado"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="risk_events", verbose_name="empresa")
    category = models.CharField("categoria", max_length=40, choices=Category.choices)
    title = models.CharField("titulo", max_length=160)
    probability = models.PositiveIntegerField("probabilidad porcentual", default=50)
    impact = models.PositiveIntegerField("impacto porcentual", default=50)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.OPEN)
    description = models.TextField("descripcion")
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "evento de riesgo"
        verbose_name_plural = "eventos de riesgo"

    @property
    def exposure_score(self):
        return round((self.probability * self.impact) / 100, 2)

    def __str__(self):
        return self.title


class RiskResponse(models.Model):
    class Strategy(models.TextChoices):
        PREVENTION = "prevencion", "Prevencion"
        MITIGATION = "mitigacion", "Mitigacion"
        RESPONSE = "respuesta", "Respuesta"
        RECOVERY = "recuperacion", "Recuperacion"

    risk_event = models.ForeignKey(RiskEvent, on_delete=models.CASCADE, related_name="responses", verbose_name="riesgo")
    strategy = models.CharField("estrategia", max_length=30, choices=Strategy.choices)
    action = models.TextField("accion")
    estimated_cost = models.DecimalField("costo estimado", max_digits=12, decimal_places=2, default=0)
    effectiveness = models.PositiveIntegerField("efectividad porcentual", default=50)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "respuesta de riesgo"
        verbose_name_plural = "respuestas de riesgo"

    def __str__(self):
        return self.get_strategy_display()

