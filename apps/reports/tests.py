from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.indicators.services import generate_company_indicators


class ReportsFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Tienda Ana", city="Bogota", target_market="Digital")
        generate_company_indicators(self.company)

    def test_dashboard_loads_for_student(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_simulation_comparison_loads_for_student(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reports:compare_simulations"))
        self.assertEqual(response.status_code, 200)

