from django.db import transaction
from django.utils import timezone

from apps.inventory.services import receive_purchase_order_into_inventory

from .models import PurchaseOrder


@transaction.atomic
def create_purchase_order(company, order_form, line_form):
    order = order_form.save(commit=False)
    order.company = company
    order.status = PurchaseOrder.Status.ORDERED
    order.save()
    order.expected_receipt_date = order.calculate_expected_receipt_date()
    order.save(update_fields=["expected_receipt_date"])

    line = line_form.save(commit=False)
    line.purchase_order = order
    line.save()
    return order


@transaction.atomic
def receive_purchase_order(order):
    order = PurchaseOrder.objects.select_for_update().get(pk=order.pk)
    if not order.can_receive:
        raise ValueError("La orden no permite recepcion.")
    receive_purchase_order_into_inventory(order)
    order.status = PurchaseOrder.Status.RECEIVED
    order.received_date = timezone.localdate()
    order.save(update_fields=["status", "received_date"])
    return order

