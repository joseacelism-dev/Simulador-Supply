from django.conf import settings
from django.db import models


class CompanyType(models.Model):
    name = models.CharField("nombre", max_length=120, unique=True)
    description = models.TextField("descripcion")
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "tipo de empresa"
        verbose_name_plural = "tipos de empresa"

    def __str__(self):
        return self.name


class Company(models.Model):
    class Difficulty(models.TextChoices):
        BASIC = "basico", "Basico"
        INTERMEDIATE = "intermedio", "Intermedio"
        ADVANCED = "avanzado", "Avanzado"
        EXPERT = "experto", "Experto"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies",
        verbose_name="estudiante",
    )
    company_type = models.ForeignKey(
        CompanyType,
        on_delete=models.PROTECT,
        related_name="companies",
        verbose_name="tipo de empresa",
    )
    name = models.CharField("nombre", max_length=160)
    country = models.CharField("pais", max_length=100, default="Colombia")
    city = models.CharField("ciudad", max_length=100)
    currency = models.CharField("moneda", max_length=10, default="COP")
    target_market = models.CharField("mercado objetivo", max_length=180)
    plants_count = models.PositiveIntegerField("numero de plantas", default=1)
    warehouses_count = models.PositiveIntegerField("numero de almacenes", default=1)
    distribution_centers_count = models.PositiveIntegerField(
        "centros de distribucion",
        default=0,
    )
    initial_capacity = models.PositiveIntegerField("capacidad inicial", default=100)
    initial_capital = models.DecimalField(
        "capital inicial",
        max_digits=14,
        decimal_places=2,
        default=0,
    )
    difficulty = models.CharField(
        "nivel de dificultad",
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BASIC,
    )
    created_at = models.DateTimeField("creada", auto_now_add=True)
    updated_at = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_company_name_per_owner",
            )
        ]

    def __str__(self):
        return self.name

