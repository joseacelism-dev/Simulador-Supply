from decimal import Decimal

from django.db import models

from apps.companies.models import Company


class FinancialTransaction(models.Model):
    class Category(models.TextChoices):
        REVENUE = "ingreso", "Ingreso"
        PURCHASE_COST = "costo_compra", "Costo de compra"
        PRODUCTION_COST = "costo_produccion", "Costo de produccion"
        STORAGE_COST = "costo_almacenamiento", "Costo de almacenamiento"
        TRANSPORT_COST = "costo_transporte", "Costo de transporte"
        RETURN_COST = "costo_devolucion", "Costo de devolucion"
        SHORTAGE_COST = "costo_faltante", "Costo por faltante"
        MAINTENANCE_COST = "costo_mantenimiento", "Costo de mantenimiento"
        OPERATING_EXPENSE = "gasto_operativo", "Gasto operativo"
        PENALTY = "penalizacion", "Penalizacion"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="financial_transactions", verbose_name="empresa")
    category = models.CharField("categoria", max_length=40, choices=Category.choices)
    description = models.CharField("descripcion", max_length=180)
    amount = models.DecimalField("valor", max_digits=14, decimal_places=2)
    transaction_date = models.DateField("fecha")
    created_at = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date", "-created_at"]
        verbose_name = "transaccion financiera"
        verbose_name_plural = "transacciones financieras"

    @property
    def signed_amount(self):
        if self.category == self.Category.REVENUE:
            return self.amount
        return self.amount * Decimal("-1")

    def __str__(self):
        return self.description


class FinancialSnapshot(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="financial_snapshots", verbose_name="empresa")
    name = models.CharField("nombre", max_length=160)
    initial_capital = models.DecimalField("capital inicial", max_digits=14, decimal_places=2)
    total_revenue = models.DecimalField("ingresos", max_digits=14, decimal_places=2, default=0)
    total_costs = models.DecimalField("costos", max_digits=14, decimal_places=2, default=0)
    profit = models.DecimalField("utilidad", max_digits=14, decimal_places=2, default=0)
    margin = models.DecimalField("margen", max_digits=6, decimal_places=2, default=0)
    cash_flow = models.DecimalField("flujo de caja", max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "resumen financiero"
        verbose_name_plural = "resumenes financieros"

    def __str__(self):
        return self.name

