from decimal import Decimal

from django.db import transaction

from .models import FinancialSnapshot, FinancialTransaction


def calculate_financial_summary(company):
    total_revenue = Decimal("0")
    total_costs = Decimal("0")
    for transaction in company.financial_transactions.all():
        if transaction.category == FinancialTransaction.Category.REVENUE:
            total_revenue += transaction.amount
        else:
            total_costs += transaction.amount
    profit = total_revenue - total_costs
    margin = Decimal("0")
    if total_revenue > 0:
        margin = (profit / total_revenue * Decimal("100")).quantize(Decimal("0.01"))
    cash_flow = Decimal(company.initial_capital) + profit
    return {
        "initial_capital": company.initial_capital,
        "total_revenue": total_revenue,
        "total_costs": total_costs,
        "profit": profit,
        "margin": margin,
        "cash_flow": cash_flow,
    }


@transaction.atomic
def create_financial_transaction(company, form):
    transaction = form.save(commit=False)
    transaction.company = company
    transaction.save()
    return transaction


@transaction.atomic
def create_financial_snapshot(company, name="Resumen financiero"):
    summary = calculate_financial_summary(company)
    return FinancialSnapshot.objects.create(company=company, name=name, **summary)

