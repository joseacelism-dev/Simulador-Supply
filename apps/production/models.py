from decimal import Decimal

from django.db import models

from apps.companies.models import Company
from apps.products.models import Product, RawMaterial


class BillOfMaterials(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="boms", verbose_name="empresa")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="boms", verbose_name="producto")
    version = models.CharField("version", max_length=40, default="1.0")
    is_active = models.BooleanField("activa", default=True)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["product__name", "version"]
        verbose_name = "BOM"
        verbose_name_plural = "BOM"
        constraints = [
            models.UniqueConstraint(fields=["company", "product", "version"], name="unique_bom_version_per_product")
        ]

    def __str__(self):
        return f"{self.product.name} v{self.version}"

    @property
    def estimated_unit_cost(self):
        total = Decimal("0")
        for line in self.lines.select_related("raw_material"):
            total += line.quantity_per_unit * line.raw_material.standard_cost
        return total


class BillOfMaterialsLine(models.Model):
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name="lines", verbose_name="BOM")
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT, related_name="bom_lines", verbose_name="materia prima")
    quantity_per_unit = models.DecimalField("cantidad por unidad", max_digits=12, decimal_places=4)
    scrap_percentage = models.DecimalField("merma porcentual", max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "linea de BOM"
        verbose_name_plural = "lineas de BOM"

    def __str__(self):
        return f"{self.raw_material.name} x {self.quantity_per_unit}"

    def required_quantity(self, production_quantity):
        base = Decimal(production_quantity) * self.quantity_per_unit
        scrap_factor = Decimal("1") + (self.scrap_percentage / Decimal("100"))
        return (base * scrap_factor).quantize(Decimal("0.01"))


class WorkCenter(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="work_centers", verbose_name="empresa")
    name = models.CharField("nombre", max_length=140)
    daily_capacity = models.DecimalField("capacidad diaria", max_digits=12, decimal_places=2)
    labor_cost_per_hour = models.DecimalField("costo hora mano de obra", max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]
        verbose_name = "centro de trabajo"
        verbose_name_plural = "centros de trabajo"

    def __str__(self):
        return self.name


class Machine(models.Model):
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE, related_name="machines", verbose_name="centro de trabajo")
    name = models.CharField("nombre", max_length=140)
    hourly_capacity = models.DecimalField("capacidad por hora", max_digits=12, decimal_places=2)
    is_available = models.BooleanField("disponible", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "maquina"
        verbose_name_plural = "maquinas"

    def __str__(self):
        return self.name


class ProductionOrder(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planificada", "Planificada"
        RELEASED = "liberada", "Liberada"
        WAITING = "en_espera", "En espera"
        IN_PROCESS = "en_proceso", "En proceso"
        PAUSED = "pausada", "Pausada"
        FINISHED = "terminada", "Terminada"
        REJECTED = "rechazada", "Rechazada"
        CANCELLED = "cancelada", "Cancelada"

    class Strategy(models.TextChoices):
        MAKE_TO_STOCK = "make_to_stock", "Make to Stock"
        MAKE_TO_ORDER = "make_to_order", "Make to Order"
        ASSEMBLE_TO_ORDER = "assemble_to_order", "Assemble to Order"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="production_orders", verbose_name="empresa")
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.PROTECT, related_name="production_orders", verbose_name="BOM")
    code = models.CharField("codigo", max_length=40)
    quantity = models.DecimalField("cantidad", max_digits=12, decimal_places=2)
    status = models.CharField("estado", max_length=30, choices=Status.choices, default=Status.PLANNED)
    strategy = models.CharField("estrategia", max_length=30, choices=Strategy.choices, default=Strategy.MAKE_TO_STOCK)
    planned_start_date = models.DateField("inicio planificado", null=True, blank=True)
    planned_end_date = models.DateField("fin planificado", null=True, blank=True)
    actual_end_date = models.DateField("fin real", null=True, blank=True)
    waste_quantity = models.DecimalField("merma", max_digits=12, decimal_places=2, default=0)
    estimated_cost = models.DecimalField("costo estimado", max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "orden de produccion"
        verbose_name_plural = "ordenes de produccion"
        constraints = [
            models.UniqueConstraint(fields=["company", "code"], name="unique_production_code_per_company")
        ]

    def __str__(self):
        return self.code

    @property
    def product(self):
        return self.bom.product

    @property
    def can_complete(self):
        return self.status in {self.Status.PLANNED, self.Status.RELEASED, self.Status.WAITING, self.Status.IN_PROCESS}

