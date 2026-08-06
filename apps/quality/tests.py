from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.customers.models import Customer
from apps.orders.models import CustomerOrder
from apps.products.models import Product

from .models import CustomerComplaint, NonConformance, QualityInspection


class QualityFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Alimentos", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Alimentos Ana", city="Bogota", target_market="Tiendas")
        self.product = Product.objects.create(company=self.company, sku="P-001", name="Producto", sale_price="10000")
        self.customer = Customer.objects.create(company=self.company, name="Cliente", segment="B2C", city="Bogota")
        self.order = CustomerOrder.objects.create(company=self.company, customer=self.customer, code="PED-001")

    def test_student_can_create_quality_inspection_with_nonconformance(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("quality:inspection_create_for_company", args=[self.company.pk]),
            {
                "code": "INSP-001",
                "product": self.product.pk,
                "inspected_quantity": "10",
                "conforming_quantity": "8",
                "nonconforming_quantity": "2",
                "notes": "Revision inicial",
                "defect_type": "Empaque danado",
                "quantity": "2",
                "root_cause": "Manipulacion",
                "corrective_action": "Refuerzo de empaque",
            },
        )

        inspection = QualityInspection.objects.get(code="INSP-001")
        self.assertRedirects(response, reverse("quality:inspection_detail", args=[inspection.pk]))
        self.assertEqual(inspection.defect_rate, 20)
        self.assertEqual(NonConformance.objects.filter(inspection=inspection).count(), 1)

    def test_student_can_create_customer_complaint(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("quality:complaint_create_for_company", args=[self.company.pk]),
            {
                "code": "REC-001",
                "order": self.order.pk,
                "product": self.product.pk,
                "reason": "Producto danado",
                "description": "El cliente reporta producto en mal estado.",
            },
        )

        complaint = CustomerComplaint.objects.get(code="REC-001")
        self.assertRedirects(response, reverse("quality:complaint_detail", args=[complaint.pk]))
        self.assertEqual(complaint.status, CustomerComplaint.Status.OPEN)

