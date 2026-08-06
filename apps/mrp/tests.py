from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.inventory.models import InventoryItem
from apps.products.models import Product, RawMaterial
from apps.production.models import BillOfMaterials

from .models import MRPPlan


class MRPFlowTests(TestCase):
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
        self.product = Product.objects.create(company=self.company, sku="BEB-001", name="Bebida", sale_price="4000")
        self.material = RawMaterial.objects.create(company=self.company, sku="AGU-001", name="Agua", standard_cost="500")
        self.bom = BillOfMaterials.objects.create(company=self.company, product=self.product)
        self.bom.lines.create(raw_material=self.material, quantity_per_unit="2", scrap_percentage="0")
        InventoryItem.objects.create(company=self.company, raw_material=self.material, quantity_available="10")

    def test_student_can_generate_mrp_plan(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("mrp:create_for_company", args=[self.company.pk]),
            {
                "name": "MRP base",
                "product": self.product.pk,
                "gross_demand": "8",
                "planned_receipt_date": "",
            },
        )

        plan = MRPPlan.objects.get(name="MRP base")
        line = plan.lines.get(raw_material=self.material)
        self.assertRedirects(response, reverse("mrp:detail", args=[plan.pk]))
        self.assertEqual(line.gross_requirement, 16)
        self.assertEqual(line.available_inventory, 10)
        self.assertEqual(line.net_requirement, 6)

