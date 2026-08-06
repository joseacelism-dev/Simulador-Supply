from django.db import models

from apps.companies.models import Company
from apps.orders.models import CustomerOrder
from apps.products.models import Product


class ReturnRequest(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "solicitada", "Solicitada"
        AUTHORIZED = "autorizada", "Autorizada"
        RECEIVED = "recibida", "Recibida"
        INSPECTED = "inspeccionada", "Inspeccionada"
        DISPOSED = "dispuesta", "Dispuesta"
        REJECTED = "rechazada", "Rechazada"
        CLOSED = "cerrada", "Cerrada"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="return_requests", verbose_name="empresa")
    order = models.ForeignKey(CustomerOrder, on_delete=models.PROTECT, related_name="returns", verbose_name="pedido")
    code = models.CharField("codigo", max_length=40)
    reason = models.CharField("motivo", max_length=180)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.REQUESTED)
    requested_at = models.DateTimeField("solicitada", auto_now_add=True)

    class Meta:
        ordering = ["-requested_at"]
        verbose_name = "solicitud de devolucion"
        verbose_name_plural = "solicitudes de devolucion"
        constraints = [models.UniqueConstraint(fields=["company", "code"], name="unique_return_code_per_company")]

    def __str__(self):
        return self.code


class ReturnLine(models.Model):
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name="lines", verbose_name="devolucion")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="return_lines", verbose_name="producto")
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2)
    condition = models.CharField("estado del producto", max_length=120, default="Pendiente de inspeccion")

    class Meta:
        verbose_name = "linea de devolucion"
        verbose_name_plural = "lineas de devolucion"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class ReturnInspection(models.Model):
    return_request = models.OneToOneField(ReturnRequest, on_delete=models.CASCADE, related_name="inspection", verbose_name="devolucion")
    accepted_quantity = models.DecimalField("cantidad aceptada", max_digits=12, decimal_places=2, default=0)
    rejected_quantity = models.DecimalField("cantidad rechazada", max_digits=12, decimal_places=2, default=0)
    notes = models.TextField("notas", blank=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        verbose_name = "inspeccion de devolucion"
        verbose_name_plural = "inspecciones de devolucion"

    def __str__(self):
        return f"Inspeccion {self.return_request.code}"


class DispositionDecision(models.Model):
    class Decision(models.TextChoices):
        RESTOCK = "reintegrar", "Reintegrar al inventario"
        REPAIR = "reparar", "Reparar"
        REFURBISH = "reacondicionar", "Reacondicionar"
        RECYCLE = "reciclar", "Reciclar"
        REUSE = "reutilizar", "Reutilizar"
        DISPOSE = "disposicion_final", "Disposicion final"
        REFUND = "reembolso", "Reembolso"
        EXCHANGE = "cambio", "Cambio"

    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name="dispositions", verbose_name="devolucion")
    decision = models.CharField("decision", max_length=40, choices=Decision.choices)
    recovered_value = models.DecimalField("valor recuperado", max_digits=12, decimal_places=2, default=0)
    environmental_impact = models.CharField("impacto ambiental", max_length=160, blank=True)
    notes = models.TextField("notas", blank=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "decision de disposicion"
        verbose_name_plural = "decisiones de disposicion"

    def __str__(self):
        return self.get_decision_display()

