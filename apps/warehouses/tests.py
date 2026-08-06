from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.products.models import Product

from .models import FinishedGoodsStock, Warehouse


class WarehouseFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Tienda Ana", city="Bogota", target_market="Digital")
        self.product = Product.objects.create(company=self.company, sku="P-001", name="Producto", sale_price="10000")

    def test_student_can_create_warehouse(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("warehouses:create_for_company", args=[self.company.pk]), {"name": "CEDI", "city": "Bogota", "capacity_units": 500})
        self.assertRedirects(response, reverse("warehouses:list"))
        self.assertTrue(Warehouse.objects.filter(company=self.company, name="CEDI").exists())

    def test_student_can_create_finished_stock(self):
        warehouse = Warehouse.objects.create(company=self.company, name="CEDI", city="Bogota")
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("warehouses:stock_create_for_company", args=[self.company.pk]),
            {"warehouse": warehouse.pk, "product": self.product.pk, "quantity_available": "25"},
        )
        self.assertRedirects(response, reverse("warehouses:stock_list"))
        self.assertTrue(FinishedGoodsStock.objects.filter(warehouse=warehouse, product=self.product, quantity_available=25).exists())

