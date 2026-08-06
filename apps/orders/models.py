from django.db import models

from apps.companies.models import Company
from apps.customers.models import Customer
from apps.products.models import Product


class CustomerOrder(models.Model):
    class Status(models.TextChoices):
        CREATED = "creado", "Creado"
        PREPARING = "preparacion", "En preparacion"
        PACKED = "empacado", "Empacado"
        DISPATCHED = "despachado", "Despachado"
        DELIVERED = "entregado", "Entregado"
        PARTIAL = "parcial", "Parcial"
        BACKORDER = "pendiente", "Pedido pendiente"
        CANCELLED = "cancelado", "Cancelado"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="customer_orders", verbose_name="empresa")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders", verbose_name="cliente")
    code = models.CharField("codigo", max_length=40)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.CREATED)
    priority = models.PositiveIntegerField("prioridad", default=3)
    promised_date = models.DateField("fecha prometida", null=True, blank=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"
        constraints = [models.UniqueConstraint(fields=["company", "code"], name="unique_order_code_per_company")]

    def __str__(self):
        return self.code

    @property
    def total_amount(self):
        return sum(line.line_total for line in self.lines.all())


class CustomerOrderLine(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name="lines", verbose_name="pedido")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_lines", verbose_name="producto")
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2)
    unit_price = models.DecimalField("precio unitario", max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "linea de pedido"
        verbose_name_plural = "lineas de pedido"

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

