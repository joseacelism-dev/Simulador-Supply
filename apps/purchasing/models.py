from datetime import timedelta

from django.db import models

from apps.companies.models import Company
from apps.products.models import RawMaterial
from apps.suppliers.models import Supplier


class PurchaseOrder(models.Model):
    class Status(models.TextChoices):
        DRAFT = "borrador", "Borrador"
        ORDERED = "ordenada", "Ordenada"
        PARTIALLY_RECEIVED = "recibida_parcial", "Recibida parcial"
        RECEIVED = "recibida", "Recibida"
        CANCELLED = "cancelada", "Cancelada"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="purchase_orders",
        verbose_name="empresa",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
        verbose_name="proveedor",
    )
    code = models.CharField("codigo", max_length=40)
    status = models.CharField(
        "estado",
        max_length=30,
        choices=Status.choices,
        default=Status.ORDERED,
    )
    order_date = models.DateField("fecha de orden", auto_now_add=True)
    expected_receipt_date = models.DateField("fecha esperada", null=True, blank=True)
    received_date = models.DateField("fecha de recepcion", null=True, blank=True)
    notes = models.TextField("notas", blank=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "orden de compra"
        verbose_name_plural = "ordenes de compra"
        constraints = [
            models.UniqueConstraint(fields=["company", "code"], name="unique_purchase_code_per_company")
        ]

    def __str__(self):
        return self.code

    @property
    def total_cost(self):
        return sum(line.line_total for line in self.lines.all())

    @property
    def can_receive(self):
        return self.status in {self.Status.ORDERED, self.Status.PARTIALLY_RECEIVED}

    def calculate_expected_receipt_date(self):
        if self.order_date:
            return self.order_date + timedelta(days=self.supplier.lead_time_days)
        return None


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="lines",
        verbose_name="orden de compra",
    )
    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.PROTECT,
        related_name="purchase_lines",
        verbose_name="materia prima",
    )
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField("costo unitario", max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "linea de orden de compra"
        verbose_name_plural = "lineas de orden de compra"

    def __str__(self):
        return f"{self.raw_material} x {self.quantity}"

    @property
    def line_total(self):
        return self.quantity * self.unit_cost

