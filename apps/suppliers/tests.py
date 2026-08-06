from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import Supplier


class SupplierFlowTests(TestCase):
    def test_student_can_create_supplier_for_own_company(self):
        user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Farmaceutica", description="Prueba")
        company = Company.objects.create(
            owner=user,
            company_type=company_type,
            name="Farma Ana",
            city="Bogota",
            target_market="Clinicas",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("suppliers:create", args=[company.pk]),
            {
                "name": "Proveedor Central",
                "location": "Bogota",
                "currency": "COP",
                "lead_time_days": 5,
                "reliability": 92,
                "quality_score": 96,
                "payment_terms": "30 dias",
                "minimum_order_quantity": 10,
                "risk_level": "Bajo",
                "certifications": "ISO 9001",
            },
        )

        self.assertRedirects(response, reverse("companies:detail", args=[company.pk]))
        self.assertTrue(Supplier.objects.filter(company=company, name="Proveedor Central").exists())

