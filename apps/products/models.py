from django.db import models

from apps.companies.models import Company


class Product(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="empresa",
    )
    sku = models.CharField("SKU", max_length=50)
    name = models.CharField("nombre", max_length=160)
    description = models.TextField("descripcion", blank=True)
    unit = models.CharField("unidad", max_length=30, default="unidad")
    sale_price = models.DecimalField("precio de venta", max_digits=12, decimal_places=2)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "producto"
        verbose_name_plural = "productos"
        constraints = [
            models.UniqueConstraint(fields=["company", "sku"], name="unique_product_sku_per_company")
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"


class RawMaterial(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="raw_materials",
        verbose_name="empresa",
    )
    sku = models.CharField("SKU", max_length=50)
    name = models.CharField("nombre", max_length=160)
    description = models.TextField("descripcion", blank=True)
    unit = models.CharField("unidad", max_length=30, default="unidad")
    standard_cost = models.DecimalField("costo estandar", max_digits=12, decimal_places=2)
    is_perishable = models.BooleanField("perecedera", default=False)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "materia prima"
        verbose_name_plural = "materias primas"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "sku"],
                name="unique_raw_material_sku_per_company",
            )
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"

