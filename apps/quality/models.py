from decimal import Decimal

from django.db import models

from apps.companies.models import Company
from apps.orders.models import CustomerOrder
from apps.products.models import Product


class QualityInspection(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planificada", "Planificada"
        COMPLETED = "completada", "Completada"
        REJECTED = "rechazada", "Rechazada"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="quality_inspections", verbose_name="empresa")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="quality_inspections", verbose_name="producto")
    code = models.CharField("codigo", max_length=40)
    inspected_quantity = models.DecimalField("cantidad inspeccionada", max_digits=12, decimal_places=2)
    conforming_quantity = models.DecimalField("cantidad conforme", max_digits=12, decimal_places=2, default=0)
    nonconforming_quantity = models.DecimalField("cantidad no conforme", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.COMPLETED)
    notes = models.TextField("notas", blank=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "inspeccion de calidad"
        verbose_name_plural = "inspecciones de calidad"
        constraints = [models.UniqueConstraint(fields=["company", "code"], name="unique_quality_inspection_code_per_company")]

    @property
    def defect_rate(self):
        if self.inspected_quantity <= 0:
            return Decimal("0")
        return (self.nonconforming_quantity / self.inspected_quantity * Decimal("100")).quantize(Decimal("0.01"))

    def __str__(self):
        return self.code


class NonConformance(models.Model):
    class Status(models.TextChoices):
        OPEN = "abierta", "Abierta"
        REVIEW = "revision", "En revision"
        RESOLVED = "resuelta", "Resuelta"
        REJECTED = "rechazada", "Rechazada"

    inspection = models.ForeignKey(QualityInspection, on_delete=models.CASCADE, related_name="nonconformances", verbose_name="inspeccion")
    defect_type = models.CharField("tipo de defecto", max_length=140)
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2)
    root_cause = models.TextField("causa raiz", blank=True)
    corrective_action = models.TextField("accion correctiva", blank=True)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "no conformidad"
        verbose_name_plural = "no conformidades"

    def __str__(self):
        return self.defect_type


class CustomerComplaint(models.Model):
    class Status(models.TextChoices):
        OPEN = "abierto", "Abierto"
        IN_PROGRESS = "en_proceso", "En proceso"
        RESOLVED = "resuelto", "Resuelto"
        CLOSED = "cerrado", "Cerrado"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="customer_complaints", verbose_name="empresa")
    order = models.ForeignKey(CustomerOrder, on_delete=models.PROTECT, related_name="complaints", verbose_name="pedido", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="complaints", verbose_name="producto")
    code = models.CharField("codigo", max_length=40)
    reason = models.CharField("motivo", max_length=180)
    description = models.TextField("descripcion")
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "reclamo de cliente"
        verbose_name_plural = "reclamos de cliente"
        constraints = [models.UniqueConstraint(fields=["company", "code"], name="unique_complaint_code_per_company")]

    def __str__(self):
        return self.code

