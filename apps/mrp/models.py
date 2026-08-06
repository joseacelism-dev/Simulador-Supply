from django.db import models

from apps.companies.models import Company
from apps.products.models import Product, RawMaterial


class MRPPlan(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="mrp_plans", verbose_name="empresa")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="mrp_plans", verbose_name="producto")
    name = models.CharField("nombre", max_length=160)
    gross_demand = models.DecimalField("demanda bruta", max_digits=12, decimal_places=2)
    planned_receipt_date = models.DateField("fecha de recepcion planificada", null=True, blank=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "plan MRP"
        verbose_name_plural = "planes MRP"

    def __str__(self):
        return self.name


class MRPLine(models.Model):
    plan = models.ForeignKey(MRPPlan, on_delete=models.CASCADE, related_name="lines", verbose_name="plan MRP")
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT, related_name="mrp_lines", verbose_name="materia prima")
    gross_requirement = models.DecimalField("necesidad bruta", max_digits=12, decimal_places=2)
    available_inventory = models.DecimalField("inventario disponible", max_digits=12, decimal_places=2)
    scheduled_receipts = models.DecimalField("recepciones programadas", max_digits=12, decimal_places=2, default=0)
    net_requirement = models.DecimalField("necesidad neta", max_digits=12, decimal_places=2)
    planned_order_quantity = models.DecimalField("orden planificada", max_digits=12, decimal_places=2)
    release_offset_days = models.PositiveIntegerField("dias antes de liberar", default=0)

    class Meta:
        ordering = ["raw_material__name"]
        verbose_name = "linea MRP"
        verbose_name_plural = "lineas MRP"

    def __str__(self):
        return f"{self.raw_material.name}: {self.net_requirement}"

