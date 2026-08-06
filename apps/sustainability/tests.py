from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import SustainabilityRecord


class SustainabilityFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Agroindustrial", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Agro Ana", city="Cali", target_market="Exportacion")

    def test_record_calculates_recovered_waste_percentage(self):
        record = SustainabilityRecord.objects.create(
            company=self.company,
            period_label="Mes 1",
            waste_kg="100",
            recovered_waste_kg="35",
            transport_emissions_kg="20",
        )

        self.assertEqual(record.recovered_waste_percentage, Decimal("35.00"))
        self.assertEqual(record.total_emissions, 20)

    def test_student_can_create_sustainability_record(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("sustainability:create_for_company", args=[self.company.pk]),
            {
                "period_label": "Mes 1",
                "energy_kwh": "120",
                "water_m3": "10",
                "waste_kg": "50",
                "recovered_waste_kg": "20",
                "transport_emissions_kg": "15",
                "recycled_material_percentage": "12",
            },
        )

        record = SustainabilityRecord.objects.get(company=self.company)
        self.assertRedirects(response, reverse("sustainability:detail", args=[record.pk]))

