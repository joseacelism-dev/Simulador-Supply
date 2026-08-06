from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.inventory.models import InventoryItem, InventoryMovement
from apps.products.models import RawMaterial
from apps.suppliers.models import Supplier

from .models import PurchaseOrder


class PurchaseFlowTests(TestCase):
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
        self.supplier = Supplier.objects.create(
            company=self.company,
            name="Proveedor Uno",
            location="Bogota",
            lead_time_days=4,
        )
        self.material = RawMaterial.objects.create(
            company=self.company,
            sku="LEC-001",
            name="Leche",
            unit="litro",
            standard_cost="1000",
        )

    def test_student_can_create_purchase_order(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("purchasing:create_for_company", args=[self.company.pk]),
            {
                "code": "OC-001",
                "supplier": self.supplier.pk,
                "notes": "Compra inicial",
                "raw_material": self.material.pk,
                "quantity": "20",
                "unit_cost": "1200",
            },
        )

        order = PurchaseOrder.objects.get(code="OC-001")
        self.assertRedirects(response, reverse("purchasing:detail", args=[order.pk]))
        self.assertEqual(order.company, self.company)
        self.assertEqual(order.lines.count(), 1)

    def test_receive_purchase_order_updates_inventory(self):
        order = PurchaseOrder.objects.create(
            company=self.company,
            supplier=self.supplier,
            code="OC-002",
        )
        order.lines.create(raw_material=self.material, quantity="15", unit_cost="1100")
        self.client.force_login(self.user)

        response = self.client.post(reverse("purchasing:receive", args=[order.pk]))

        self.assertRedirects(response, reverse("purchasing:detail", args=[order.pk]))
        order.refresh_from_db()
        item = InventoryItem.objects.get(company=self.company, raw_material=self.material)
        self.assertEqual(order.status, PurchaseOrder.Status.RECEIVED)
        self.assertEqual(item.quantity_available, 15)
        self.assertEqual(InventoryMovement.objects.filter(inventory_item=item).count(), 1)

