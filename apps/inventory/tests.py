from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.products.models import RawMaterial

from .models import InventoryPolicy


class InventoryPolicyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Alimentos", description="Prueba")
        self.company = Company.objects.create(
            owner=self.user,
            company_type=company_type,
            name="Alimentos Ana",
            city="Bogota",
            target_market="Supermercados",
        )
        self.material = RawMaterial.objects.create(
            company=self.company,
            sku="LEC-001",
            name="Leche",
            unit="litro",
            standard_cost="1000",
        )

    def test_policy_calculates_eoq_and_reorder_point(self):
        policy = InventoryPolicy.objects.create(
            company=self.company,
            raw_material=self.material,
            annual_demand="1200",
            ordering_cost="50000",
            holding_cost="2000",
            daily_demand="4",
            lead_time_days=5,
            safety_stock="10",
        )

        self.assertEqual(policy.eoq, Decimal("244.95"))
        self.assertEqual(policy.reorder_point, Decimal("30.00"))

    def test_student_can_create_inventory_policy(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("inventory:policy_create_for_company", args=[self.company.pk]),
            {
                "raw_material": self.material.pk,
                "annual_demand": "1200",
                "ordering_cost": "50000",
                "holding_cost": "2000",
                "daily_demand": "4",
                "lead_time_days": 5,
                "safety_stock": "10",
            },
        )

        self.assertRedirects(response, reverse("inventory:policy_create_for_company", args=[self.company.pk]))
        self.assertTrue(InventoryPolicy.objects.filter(company=self.company, raw_material=self.material).exists())
