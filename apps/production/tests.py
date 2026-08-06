from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.inventory.models import InventoryItem, InventoryMovement
from apps.products.models import Product, RawMaterial

from .models import BillOfMaterials, ProductionOrder


class ProductionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Confecciones", description="Prueba")
        self.company = Company.objects.create(
            owner=self.user,
            company_type=company_type,
            name="Moda Ana",
            city="Medellin",
            target_market="Tiendas",
        )
        self.product = Product.objects.create(company=self.company, sku="CAM-001", name="Camisa", sale_price="50000")
        self.material = RawMaterial.objects.create(company=self.company, sku="TEL-001", name="Tela", standard_cost="8000")

    def test_student_can_create_bom(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("production:bom_create_for_company", args=[self.company.pk]),
            {
                "product": self.product.pk,
                "version": "1.0",
                "is_active": "on",
                "raw_material": self.material.pk,
                "quantity_per_unit": "2",
                "scrap_percentage": "5",
            },
        )

        bom = BillOfMaterials.objects.get(product=self.product)
        self.assertRedirects(response, reverse("production:bom_detail", args=[bom.pk]))
        self.assertEqual(bom.lines.count(), 1)

    def test_complete_order_consumes_inventory(self):
        bom = BillOfMaterials.objects.create(company=self.company, product=self.product)
        bom.lines.create(raw_material=self.material, quantity_per_unit="2", scrap_percentage="0")
        InventoryItem.objects.create(company=self.company, raw_material=self.material, quantity_available="20")
        order = ProductionOrder.objects.create(company=self.company, bom=bom, code="OP-001", quantity="4")
        self.client.force_login(self.user)

        response = self.client.post(reverse("production:order_complete", args=[order.pk]))

        self.assertRedirects(response, reverse("production:order_detail", args=[order.pk]))
        order.refresh_from_db()
        item = InventoryItem.objects.get(company=self.company, raw_material=self.material)
        self.assertEqual(order.status, ProductionOrder.Status.FINISHED)
        self.assertEqual(item.quantity_available, 12)
        self.assertEqual(InventoryMovement.objects.filter(inventory_item=item).count(), 1)

    def test_order_with_shortage_is_not_completed(self):
        bom = BillOfMaterials.objects.create(company=self.company, product=self.product)
        bom.lines.create(raw_material=self.material, quantity_per_unit="5", scrap_percentage="0")
        InventoryItem.objects.create(company=self.company, raw_material=self.material, quantity_available="3")
        order = ProductionOrder.objects.create(company=self.company, bom=bom, code="OP-002", quantity="2")
        self.client.force_login(self.user)

        self.client.post(reverse("production:order_complete", args=[order.pk]))

        order.refresh_from_db()
        self.assertEqual(order.status, ProductionOrder.Status.WAITING)

