from django.db import models

from apps.companies.models import Company
from apps.orders.models import CustomerOrder
from apps.warehouses.models import Warehouse


class Carrier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="carriers", verbose_name="empresa")
    name = models.CharField("nombre", max_length=160)
    service_level = models.PositiveIntegerField("nivel de servicio", default=90)
    cost_per_km = models.DecimalField("costo por km", max_digits=12, decimal_places=2, default=0)
    risk_level = models.CharField("nivel de riesgo", max_length=80, default="Medio")

    class Meta:
        ordering = ["name"]
        verbose_name = "transportador"
        verbose_name_plural = "transportadores"
        constraints = [models.UniqueConstraint(fields=["company", "name"], name="unique_carrier_name_per_company")]

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name="vehicles", verbose_name="transportador")
    plate = models.CharField("placa", max_length=30)
    weight_capacity = models.DecimalField("capacidad peso", max_digits=12, decimal_places=2, default=0)
    volume_capacity = models.DecimalField("capacidad volumen", max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["plate"]
        verbose_name = "vehiculo"
        verbose_name_plural = "vehiculos"

    def __str__(self):
        return self.plate


class Route(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="routes", verbose_name="empresa")
    name = models.CharField("nombre", max_length=160)
    origin_city = models.CharField("ciudad origen", max_length=100)
    destination_city = models.CharField("ciudad destino", max_length=100)
    distance_km = models.DecimalField("distancia km", max_digits=12, decimal_places=2)
    estimated_days = models.PositiveIntegerField("dias estimados", default=1)
    risk_level = models.CharField("nivel de riesgo", max_length=80, default="Medio")

    class Meta:
        ordering = ["name"]
        verbose_name = "ruta"
        verbose_name_plural = "rutas"

    def __str__(self):
        return self.name


class Shipment(models.Model):
    class Status(models.TextChoices):
        CREATED = "creado", "Creado"
        DISPATCHED = "despachado", "Despachado"
        IN_TRANSIT = "en_transito", "En transito"
        DELIVERED = "entregado", "Entregado"
        FAILED = "fallido", "Entrega fallida"
        CANCELLED = "cancelado", "Cancelado"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="shipments", verbose_name="empresa")
    order = models.ForeignKey(CustomerOrder, on_delete=models.PROTECT, related_name="shipments", verbose_name="pedido")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="shipments", verbose_name="almacen")
    carrier = models.ForeignKey(Carrier, on_delete=models.PROTECT, related_name="shipments", verbose_name="transportador")
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name="shipments", verbose_name="ruta")
    code = models.CharField("codigo", max_length=40)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.DISPATCHED)
    dispatch_date = models.DateField("fecha despacho", auto_now_add=True)
    delivered_date = models.DateField("fecha entrega", null=True, blank=True)
    shipping_cost = models.DecimalField("costo de transporte", max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["-dispatch_date"]
        verbose_name = "despacho"
        verbose_name_plural = "despachos"
        constraints = [models.UniqueConstraint(fields=["company", "code"], name="unique_shipment_code_per_company")]

    def __str__(self):
        return self.code

