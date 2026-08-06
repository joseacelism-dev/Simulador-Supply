from decimal import Decimal

from django.db import models

from apps.companies.models import Company


class SustainabilityRecord(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sustainability_records", verbose_name="empresa")
    period_label = models.CharField("periodo", max_length=80)
    energy_kwh = models.DecimalField("energia kWh", max_digits=12, decimal_places=2, default=0)
    water_m3 = models.DecimalField("agua m3", max_digits=12, decimal_places=2, default=0)
    waste_kg = models.DecimalField("residuos kg", max_digits=12, decimal_places=2, default=0)
    recovered_waste_kg = models.DecimalField("residuos recuperados kg", max_digits=12, decimal_places=2, default=0)
    transport_emissions_kg = models.DecimalField("emisiones transporte kg CO2e", max_digits=12, decimal_places=2, default=0)
    recycled_material_percentage = models.DecimalField("material reciclado porcentual", max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "registro de sostenibilidad"
        verbose_name_plural = "registros de sostenibilidad"

    @property
    def total_emissions(self):
        return Decimal(self.transport_emissions_kg)

    @property
    def recovered_waste_percentage(self):
        waste_kg = Decimal(self.waste_kg)
        recovered_waste_kg = Decimal(self.recovered_waste_kg)
        if waste_kg <= 0:
            return Decimal("0")
        return (recovered_waste_kg / waste_kg * Decimal("100")).quantize(Decimal("0.01"))

    def __str__(self):
        return f"{self.company.name} - {self.period_label}"
