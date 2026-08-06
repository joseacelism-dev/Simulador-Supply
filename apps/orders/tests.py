from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.customers.models import Customer
from apps.products.models import Product

from .models import CustomerOrder


class CustomerOrderFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Tienda Ana", city="Bogota", target_market="Digital")
        self.customer = Customer.objects.create(company=self.company, name="Cliente Uno", segment="B2C", city="Bogota")
        self.product = Product.objects.create(company=self.company, sku="P-001", name="Producto", sale_price="10000")

    def test_student_can_create_customer_order(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("orders:create_for_company", args=[self.company.pk]),
            {
                "code": "PED-001",
                "customer": self.customer.pk,
                "priority": 2,
                "promised_date": "",
                "product": self.product.pk,
                "quantity": "3",
                "unit_price": "10000",
            },
        )

        order = CustomerOrder.objects.get(code="PED-001")
        self.assertRedirects(response, reverse("orders:detail", args=[order.pk]))
        self.assertEqual(order.lines.count(), 1)

