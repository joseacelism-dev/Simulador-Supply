from decimal import Decimal

from django.db import transaction

from apps.inventory.models import InventoryItem
from apps.production.models import BillOfMaterials
from apps.purchasing.models import PurchaseOrder

from .models import MRPLine


@transaction.atomic
def create_mrp_plan(company, form):
    plan = form.save(commit=False)
    plan.company = company
    plan.save()
    generate_mrp_lines(plan)
    return plan


def generate_mrp_lines(plan):
    bom = BillOfMaterials.objects.filter(company=plan.company, product=plan.product, is_active=True).first()
    if bom is None:
        raise ValueError("El producto no tiene una BOM activa.")

    MRPLine.objects.filter(plan=plan).delete()
    for bom_line in bom.lines.select_related("raw_material"):
        gross_requirement = bom_line.required_quantity(plan.gross_demand)
        available = _get_available_inventory(plan.company, bom_line.raw_material)
        scheduled = _get_scheduled_receipts(plan.company, bom_line.raw_material)
        net = gross_requirement - available - scheduled
        if net < 0:
            net = Decimal("0")
        MRPLine.objects.create(
            plan=plan,
            raw_material=bom_line.raw_material,
            gross_requirement=gross_requirement,
            available_inventory=available,
            scheduled_receipts=scheduled,
            net_requirement=net,
            planned_order_quantity=net,
            release_offset_days=_get_release_offset_days(plan.company, bom_line.raw_material),
        )


def _get_available_inventory(company, raw_material):
    item = InventoryItem.objects.filter(company=company, raw_material=raw_material).first()
    return item.quantity_available if item else Decimal("0")


def _get_scheduled_receipts(company, raw_material):
    total = Decimal("0")
    orders = PurchaseOrder.objects.filter(
        company=company,
        status__in=[PurchaseOrder.Status.ORDERED, PurchaseOrder.Status.PARTIALLY_RECEIVED],
        lines__raw_material=raw_material,
    ).distinct()
    for order in orders:
        for line in order.lines.filter(raw_material=raw_material):
            total += line.quantity
    return total


def _get_release_offset_days(company, raw_material):
    policy = company.inventory_policies.filter(raw_material=raw_material).first()
    if policy:
        return policy.lead_time_days
    return 0

