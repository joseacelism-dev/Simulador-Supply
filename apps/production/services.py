from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.inventory.models import InventoryItem, InventoryMovement

from .models import ProductionOrder


def calculate_required_materials(bom, quantity):
    requirements = []
    for line in bom.lines.select_related("raw_material"):
        requirements.append(
            {
                "raw_material": line.raw_material,
                "required_quantity": line.required_quantity(quantity),
                "line": line,
            }
        )
    return requirements


def get_material_shortages(order):
    shortages = []
    for requirement in calculate_required_materials(order.bom, order.quantity):
        item = InventoryItem.objects.filter(
            company=order.company,
            raw_material=requirement["raw_material"],
        ).first()
        available = item.quantity_available if item else Decimal("0")
        if available < requirement["required_quantity"]:
            shortages.append(
                {
                    "raw_material": requirement["raw_material"],
                    "required": requirement["required_quantity"],
                    "available": available,
                    "shortage": requirement["required_quantity"] - available,
                }
            )
    return shortages


@transaction.atomic
def create_bom(company, bom_form, line_form):
    bom = bom_form.save(commit=False)
    bom.company = company
    bom.save()
    line = line_form.save(commit=False)
    line.bom = bom
    line.save()
    return bom


@transaction.atomic
def create_production_order(company, form):
    order = form.save(commit=False)
    order.company = company
    order.estimated_cost = order.bom.estimated_unit_cost * order.quantity
    order.save()
    return order


def complete_production_order(order):
    order = ProductionOrder.objects.select_related("bom", "company").get(pk=order.pk)
    if not order.can_complete:
        raise ValueError("La orden no permite completarse.")
    shortages = get_material_shortages(order)
    if shortages:
        order.status = ProductionOrder.Status.WAITING
        order.save(update_fields=["status"])
        raise ValueError("Inventario insuficiente para completar la orden.")

    with transaction.atomic():
        order = ProductionOrder.objects.select_for_update().select_related("bom", "company").get(pk=order.pk)
        for requirement in calculate_required_materials(order.bom, order.quantity):
            item = InventoryItem.objects.select_for_update().get(
                company=order.company,
                raw_material=requirement["raw_material"],
            )
            item.quantity_available -= requirement["required_quantity"]
            item.save(update_fields=["quantity_available", "last_updated"])
            InventoryMovement.objects.create(
                inventory_item=item,
                movement_type=InventoryMovement.MovementType.PRODUCTION_CONSUMPTION,
                quantity=requirement["required_quantity"],
                unit_cost=requirement["raw_material"].standard_cost,
                reference=order.code,
            )

        order.status = ProductionOrder.Status.FINISHED
        order.actual_end_date = timezone.localdate()
        order.save(update_fields=["status", "actual_end_date"])
    return order
