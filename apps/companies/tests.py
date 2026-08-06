from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User

from .models import Company, CompanyType


class CompanyFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company_type = CompanyType.objects.create(
            name="Empresa de prueba",
            description="Tipo de prueba",
        )

    def test_student_can_create_company(self):
        user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        self.client.force_login(user)

        response = self.client.post(
            reverse("companies:create"),
            {
                "name": "Alimentos Ana",
                "company_type": self.company_type.pk,
                "country": "Colombia",
                "city": "Bogota",
                "currency": "COP",
                "target_market": "Supermercados",
                "plants_count": 1,
                "warehouses_count": 1,
                "distribution_centers_count": 0,
                "initial_capacity": 100,
                "initial_capital": "5000000",
                "difficulty": Company.Difficulty.BASIC,
            },
        )

        self.assertRedirects(response, reverse("companies:list"))
        self.assertTrue(Company.objects.filter(owner=user, name="Alimentos Ana").exists())

    def test_student_cannot_view_another_student_company(self):
        owner = User.objects.create_user(username="owner", password="ClaveSegura123!")
        visitor = User.objects.create_user(username="visitor", password="ClaveSegura123!")
        company = Company.objects.create(
            owner=owner,
            company_type=self.company_type,
            name="Empresa privada",
            city="Cali",
            target_market="Tiendas",
        )
        self.client.force_login(visitor)

        response = self.client.get(reverse("companies:detail", args=[company.pk]))

        self.assertEqual(response.status_code, 404)

    def test_teacher_can_view_company_list(self):
        teacher = User.objects.create_user(
            username="docente",
            password="ClaveSegura123!",
            role=User.Role.ADMIN_DOCENTE,
            is_staff=True,
        )
        self.client.force_login(teacher)

        response = self.client.get(reverse("companies:teacher_list"))

        self.assertEqual(response.status_code, 200)


class CompanyTypeSeedTests(TestCase):
    def test_initial_company_types_exist(self):
        expected_names = {
            "Empresa de alimentos procesados",
            "Empresa de confecciones",
            "Empresa farmaceutica",
            "Empresa de comercio electronico",
            "Empresa agroindustrial y exportadora",
        }

        existing_names = set(CompanyType.objects.values_list("name", flat=True))

        self.assertTrue(expected_names.issubset(existing_names))
