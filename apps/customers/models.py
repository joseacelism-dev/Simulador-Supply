from django.db import models

from apps.companies.models import Company


class Customer(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customers",
        verbose_name="empresa",
    )
    name = models.CharField("nombre", max_length=160)
    segment = models.CharField("segmento", max_length=120)
    city = models.CharField("ciudad", max_length=100)
    country = models.CharField("pais", max_length=100, default="Colombia")
    expected_service_level = models.PositiveIntegerField("nivel de servicio esperado", default=95)
    payment_terms = models.CharField("condiciones de pago", max_length=120, blank=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        constraints = [
            models.UniqueConstraint(fields=["company", "name"], name="unique_customer_name_per_company")
        ]

    def __str__(self):
        return self.name

