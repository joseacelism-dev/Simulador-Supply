from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.customers.models import Customer
from apps.orders.models import CustomerOrder
from apps.products.models import Product

from .models import DispositionDecision, ReturnInspection, ReturnRequest


class ReverseLogisticsFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Tienda Ana", city="Bogota", target_market="Digital")
        self.customer = Customer.objects.create(company=self.company, name="Cliente", segment="B2C", city="Bogota")
        self.product = Product.objects.create(company=self.company, sku="P-001", name="Producto", sale_price="10000")
        self.order = CustomerOrder.objects.create(company=self.company, customer=self.customer, code="PED-001")

    def test_student_can_create_return_request(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("reverse_logistics:return_create_for_company", args=[self.company.pk]),
            {
                "code": "DEV-001",
                "order": self.order.pk,
                "reason": "Cambio solicitado",
                "product": self.product.pk,
                "quantity": "1",
                "condition": "Sin uso",
            },
        )

        return_request = ReturnRequest.objects.get(code="DEV-001")
        self.assertRedirects(response, reverse("reverse_logistics:return_detail", args=[return_request.pk]))
        self.assertEqual(return_request.lines.count(), 1)

    def test_student_can_inspect_and_dispose_return(self):
        return_request = ReturnRequest.objects.create(company=self.company, order=self.order, code="DEV-002", reason="Garantia")
        self.client.force_login(self.user)

        inspect_response = self.client.post(
            reverse("reverse_logistics:return_inspect", args=[return_request.pk]),
            {"accepted_quantity": "1", "rejected_quantity": "0", "notes": "Producto recuperable"},
        )
        dispose_response = self.client.post(
            reverse("reverse_logistics:return_dispose", args=[return_request.pk]),
            {
                "decision": DispositionDecision.Decision.RESTOCK,
                "recovered_value": "7000",
                "environmental_impact": "Bajo",
                "notes": "Se reintegra.",
            },
        )

        return_request.refresh_from_db()
        self.assertRedirects(inspect_response, reverse("reverse_logistics:return_detail", args=[return_request.pk]))
        self.assertRedirects(dispose_response, reverse("reverse_logistics:return_detail", args=[return_request.pk]))
        self.assertTrue(ReturnInspection.objects.filter(return_request=return_request).exists())
        self.assertEqual(return_request.status, ReturnRequest.Status.DISPOSED)
        self.assertEqual(return_request.dispositions.first().recovered_value, 7000)

