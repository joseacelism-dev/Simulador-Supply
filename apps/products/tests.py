from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import Product, RawMaterial


class ProductFlowTests(TestCase):
    def test_student_can_create_product_for_own_company(self):
        user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Confecciones", description="Prueba")
        company = Company.objects.create(
            owner=user,
            company_type=company_type,
            name="Moda Ana",
            city="Medellin",
            target_market="Tiendas",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("products:create", args=[company.pk]),
            {
                "sku": "CAM-001",
                "name": "Camisa basica",
                "description": "Producto de prueba",
                "unit": "unidad",
                "sale_price": "45000",
            },
        )

        self.assertRedirects(response, reverse("companies:detail", args=[company.pk]))
        self.assertTrue(Product.objects.filter(company=company, sku="CAM-001").exists())

    def test_student_can_create_raw_material_for_own_company(self):
        user = User.objects.create_user(username="luis", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Alimentos", description="Prueba")
        company = Company.objects.create(
            owner=user,
            company_type=company_type,
            name="Alimentos Luis",
            city="Bogota",
            target_market="Supermercados",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("products:raw_material_create", args=[company.pk]),
            {
                "sku": "LEC-001",
                "name": "Leche cruda",
                "description": "Materia prima de prueba",
                "unit": "litro",
                "standard_cost": "1800",
                "is_perishable": "on",
            },
        )

        self.assertRedirects(response, reverse("companies:detail", args=[company.pk]))
        self.assertTrue(RawMaterial.objects.filter(company=company, sku="LEC-001").exists())
