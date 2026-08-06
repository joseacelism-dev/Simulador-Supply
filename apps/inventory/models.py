from decimal import Decimal

from django.db import models

from apps.companies.models import Company
from apps.products.models import RawMaterial


class InventoryItem(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="inventory_items",
        verbose_name="empresa",
    )
    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.CASCADE,
        related_name="inventory_items",
        verbose_name="materia prima",
    )
    quantity_available = models.DecimalField("disponible", max_digits=12, decimal_places=2, default=0)
    quantity_committed = models.DecimalField("comprometido", max_digits=12, decimal_places=2, default=0)
    quantity_in_transit = models.DecimalField("en transito", max_digits=12, decimal_places=2, default=0)
    damaged_quantity = models.DecimalField("averiado", max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        ordering = ["raw_material__name"]
        verbose_name = "item de inventario"
        verbose_name_plural = "items de inventario"
        constraints = [
            models.UniqueConstraint(fields=["company", "raw_material"], name="unique_inventory_item_per_material")
        ]

    def __str__(self):
        return f"{self.raw_material} - {self.quantity_available}"

    @property
    def net_available(self):
        return self.quantity_available - self.quantity_committed


class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        PURCHASE_RECEIPT = "recepcion_compra", "Recepcion de compra"
        ADJUSTMENT_IN = "ajuste_entrada", "Ajuste de entrada"
        ADJUSTMENT_OUT = "ajuste_salida", "Ajuste de salida"

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="movements",
        verbose_name="item de inventario",
    )
    movement_type = models.CharField("tipo", max_length=40, choices=MovementType.choices)
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField("costo unitario", max_digits=12, decimal_places=2, default=0)
    reference = models.CharField("referencia", max_length=120, blank=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "movimiento de inventario"
        verbose_name_plural = "movimientos de inventario"

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity}"


class InventoryPolicy(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="inventory_policies",
        verbose_name="empresa",
    )
    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.CASCADE,
        related_name="inventory_policies",
        verbose_name="materia prima",
    )
    annual_demand = models.DecimalField("demanda anual", max_digits=12, decimal_places=2)
    ordering_cost = models.DecimalField("costo de ordenar", max_digits=12, decimal_places=2)
    holding_cost = models.DecimalField("costo anual de mantener", max_digits=12, decimal_places=2)
    daily_demand = models.DecimalField("demanda diaria", max_digits=12, decimal_places=2)
    lead_time_days = models.PositiveIntegerField("lead time en dias")
    safety_stock = models.DecimalField("stock de seguridad", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField("creada", auto_now_add=True)
    updated_at = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        ordering = ["raw_material__name"]
        verbose_name = "politica de inventario"
        verbose_name_plural = "politicas de inventario"
        constraints = [
            models.UniqueConstraint(fields=["company", "raw_material"], name="unique_inventory_policy_per_material")
        ]

    def __str__(self):
        return f"Politica {self.raw_material}"

    @property
    def eoq(self):
        annual_demand = Decimal(self.annual_demand)
        ordering_cost = Decimal(self.ordering_cost)
        holding_cost = Decimal(self.holding_cost)
        if holding_cost <= 0:
            return Decimal("0")
        value = (Decimal("2") * annual_demand * ordering_cost) / holding_cost
        return Decimal(value).sqrt().quantize(Decimal("0.01"))

    @property
    def reorder_point(self):
        daily_demand = Decimal(self.daily_demand)
        safety_stock = Decimal(self.safety_stock)
        return (daily_demand * Decimal(self.lead_time_days) + safety_stock).quantize(Decimal("0.01"))

    def is_below_reorder_point(self, inventory_item):
        return inventory_item.quantity_available <= self.reorder_point
