from datetime import date

from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.customers.models import Customer
from apps.finance.models import FinancialTransaction
from apps.orders.models import CustomerOrder
from apps.products.models import Product

from .models import Indicator
from .services import generate_company_indicators


class IndicatorFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Tienda Ana", city="Bogota", target_market="Digital")
        self.customer = Customer.objects.create(company=self.company, name="Cliente", segment="B2C", city="Bogota")
        self.product = Product.objects.create(company=self.company, sku="P-001", name="Producto", sale_price="10000")
        CustomerOrder.objects.create(company=self.company, customer=self.customer, code="PED-001", status=CustomerOrder.Status.DELIVERED)
        FinancialTransaction.objects.create(company=self.company, category=FinancialTransaction.Category.REVENUE, description="Venta", amount="1000", transaction_date=date.today())

    def test_generate_company_indicators(self):
        indicators = generate_company_indicators(self.company)
        self.assertEqual(len(indicators), 10)
        self.assertTrue(Indicator.objects.filter(company=self.company, code="service_level").exists())

    def test_export_csv(self):
        generate_company_indicators(self.company)
        self.client.force_login(self.user)
        response = self.client.get(reverse("indicators:export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])

