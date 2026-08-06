from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import RiskEvent, RiskResponse


class RiskFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Alimentos", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Alimentos Ana", city="Bogota", target_market="Tiendas")

    def test_student_can_create_risk(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("risks:create_for_company", args=[self.company.pk]),
            {
                "category": RiskEvent.Category.SUPPLIER_DELAY,
                "title": "Retraso proveedor",
                "probability": 60,
                "impact": 70,
                "description": "Proveedor critico puede retrasarse.",
            },
        )

        risk = RiskEvent.objects.get(title="Retraso proveedor")
        self.assertRedirects(response, reverse("risks:detail", args=[risk.pk]))
        self.assertEqual(risk.exposure_score, 42)

    def test_response_mitigates_risk(self):
        risk = RiskEvent.objects.create(company=self.company, category=RiskEvent.Category.CLIMATE, title="Clima", probability=50, impact=80, description="Lluvias")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("risks:response_create", args=[risk.pk]),
            {
                "strategy": RiskResponse.Strategy.MITIGATION,
                "action": "Proveedor alterno",
                "estimated_cost": "200",
                "effectiveness": 75,
            },
        )

        risk.refresh_from_db()
        self.assertRedirects(response, reverse("risks:detail", args=[risk.pk]))
        self.assertEqual(risk.status, RiskEvent.Status.MITIGATED)

