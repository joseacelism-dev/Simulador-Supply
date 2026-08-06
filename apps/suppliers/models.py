from django.db import models

from apps.companies.models import Company


class Supplier(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="suppliers",
        verbose_name="empresa",
    )
    name = models.CharField("nombre", max_length=160)
    location = models.CharField("ubicacion", max_length=160)
    currency = models.CharField("moneda", max_length=10, default="COP")
    lead_time_days = models.PositiveIntegerField("lead time en dias", default=7)
    reliability = models.PositiveIntegerField("confiabilidad porcentual", default=90)
    quality_score = models.PositiveIntegerField("calidad porcentual", default=90)
    payment_terms = models.CharField("condiciones de pago", max_length=120, blank=True)
    minimum_order_quantity = models.PositiveIntegerField("cantidad minima de pedido", default=1)
    risk_level = models.CharField("nivel de riesgo", max_length=80, default="Medio")
    certifications = models.CharField("certificaciones", max_length=240, blank=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        constraints = [
            models.UniqueConstraint(fields=["company", "name"], name="unique_supplier_name_per_company")
        ]

    def __str__(self):
        return self.name

