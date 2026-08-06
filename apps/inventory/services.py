from django.db import transaction

from .models import InventoryItem, InventoryMovement


@transaction.atomic
def receive_purchase_order_into_inventory(order):
    for line in order.lines.select_related("raw_material"):
        item, _ = InventoryItem.objects.select_for_update().get_or_create(
            company=order.company,
            raw_material=line.raw_material,
            defaults={"quantity_available": 0},
        )
        item.quantity_available += line.quantity
        item.save(update_fields=["quantity_available", "last_updated"])
        InventoryMovement.objects.create(
            inventory_item=item,
            movement_type=InventoryMovement.MovementType.PURCHASE_RECEIPT,
            quantity=line.quantity,
            unit_cost=line.unit_cost,
            reference=order.code,
        )


def get_inventory_alerts(company):
    alerts = []
    policies = company.inventory_policies.select_related("raw_material")
    for policy in policies:
        item, _ = InventoryItem.objects.get_or_create(
            company=company,
            raw_material=policy.raw_material,
            defaults={"quantity_available": 0},
        )
        if policy.is_below_reorder_point(item):
            alerts.append(
                {
                    "material": policy.raw_material,
                    "available": item.quantity_available,
                    "reorder_point": policy.reorder_point,
                    "message": "Inventario bajo o en punto de reorden.",
                }
            )
    return alerts

