from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import FinancialSnapshot, FinancialTransaction
from .services import calculate_financial_summary


class FinanceFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(
            owner=self.user,
            company_type=company_type,
            name="Tienda Ana",
            city="Bogota",
            target_market="Digital",
            initial_capital="1000",
        )

    def test_financial_summary_calculates_profit_and_cash_flow(self):
        FinancialTransaction.objects.create(company=self.company, category=FinancialTransaction.Category.REVENUE, description="Venta", amount="500", transaction_date=date.today())
        FinancialTransaction.objects.create(company=self.company, category=FinancialTransaction.Category.TRANSPORT_COST, description="Flete", amount="150", transaction_date=date.today())

        summary = calculate_financial_summary(self.company)

        self.assertEqual(summary["profit"], Decimal("350"))
        self.assertEqual(summary["cash_flow"], Decimal("1350"))
        self.assertEqual(summary["margin"], Decimal("70.00"))

    def test_student_can_create_financial_transaction(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("finance:transaction_create_for_company", args=[self.company.pk]),
            {
                "category": FinancialTransaction.Category.REVENUE,
                "description": "Venta inicial",
                "amount": "800",
                "transaction_date": date.today().isoformat(),
            },
        )

        self.assertRedirects(response, reverse("finance:snapshot_list"))
        self.assertTrue(FinancialSnapshot.objects.filter(company=self.company).exists())

