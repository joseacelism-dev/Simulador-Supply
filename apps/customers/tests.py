from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import Customer


class CustomerFlowTests(TestCase):
    def test_student_can_create_customer_for_own_company(self):
        user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        company = Company.objects.create(
            owner=user,
            company_type=company_type,
            name="Tienda Ana",
            city="Medellin",
            target_market="Clientes digitales",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("customers:create", args=[company.pk]),
            {
                "name": "Cliente Mayorista",
                "segment": "B2B",
                "city": "Cali",
                "country": "Colombia",
                "expected_service_level": 95,
                "payment_terms": "Contado",
            },
        )

        self.assertRedirects(response, reverse("companies:detail", args=[company.pk]))
        self.assertTrue(Customer.objects.filter(company=company, name="Cliente Mayorista").exists())

