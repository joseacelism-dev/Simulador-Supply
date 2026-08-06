from django.db import models

from apps.companies.models import Company
from apps.products.models import Product


class Warehouse(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="warehouses", verbose_name="empresa")
    name = models.CharField("nombre", max_length=160)
    city = models.CharField("ciudad", max_length=100)
    capacity_units = models.PositiveIntegerField("capacidad en unidades", default=1000)
    is_distribution_center = models.BooleanField("centro de distribucion", default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "almacen"
        verbose_name_plural = "almacenes"
        constraints = [models.UniqueConstraint(fields=["company", "name"], name="unique_warehouse_name_per_company")]

    def __str__(self):
        return self.name


class WarehouseLocation(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="locations", verbose_name="almacen")
    code = models.CharField("codigo", max_length=40)
    zone = models.CharField("zona", max_length=80, blank=True)
    capacity_units = models.PositiveIntegerField("capacidad en unidades", default=100)

    class Meta:
        ordering = ["code"]
        verbose_name = "ubicacion"
        verbose_name_plural = "ubicaciones"
        constraints = [models.UniqueConstraint(fields=["warehouse", "code"], name="unique_location_code_per_warehouse")]

    def __str__(self):
        return f"{self.warehouse.name} - {self.code}"


class FinishedGoodsStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="finished_goods", verbose_name="almacen")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="finished_stocks", verbose_name="producto")
    quantity_available = models.DecimalField("disponible", max_digits=12, decimal_places=2, default=0)
    quantity_committed = models.DecimalField("comprometido", max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["product__name"]
        verbose_name = "stock de producto terminado"
        verbose_name_plural = "stock de producto terminado"
        constraints = [models.UniqueConstraint(fields=["warehouse", "product"], name="unique_finished_stock_per_warehouse")]

    @property
    def net_available(self):
        return self.quantity_available - self.quantity_committed

    def __str__(self):
        return f"{self.product.name} - {self.quantity_available}"

