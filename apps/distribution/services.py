from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.orders.models import CustomerOrder
from apps.warehouses.models import FinishedGoodsStock

from .models import Shipment


def calculate_shipping_cost(carrier, route):
    return (Decimal(carrier.cost_per_km) * Decimal(route.distance_km)).quantize(Decimal("0.01"))


def get_order_stock_shortages(order, warehouse):
    shortages = []
    for line in order.lines.select_related("product"):
        stock = FinishedGoodsStock.objects.filter(warehouse=warehouse, product=line.product).first()
        available = stock.quantity_available if stock else Decimal("0")
        if available < line.quantity:
            shortages.append(
                {
                    "product": line.product,
                    "required": line.quantity,
                    "available": available,
                    "shortage": line.quantity - available,
                }
            )
    return shortages


def create_shipment(company, form):
    shipment = form.save(commit=False)
    shipment.company = company
    shipment.shipping_cost = calculate_shipping_cost(shipment.carrier, shipment.route)
    shortages = get_order_stock_shortages(shipment.order, shipment.warehouse)
    if shortages:
        shipment.order.status = CustomerOrder.Status.BACKORDER
        shipment.order.save(update_fields=["status"])
        raise ValueError("Stock insuficiente para despachar el pedido.")

    with transaction.atomic():
        shipment.save()
        for line in shipment.order.lines.select_related("product"):
            stock = FinishedGoodsStock.objects.select_for_update().get(
                warehouse=shipment.warehouse,
                product=line.product,
            )
            stock.quantity_available -= line.quantity
            stock.quantity_committed += line.quantity
            stock.save(update_fields=["quantity_available", "quantity_committed"])
        shipment.order.status = CustomerOrder.Status.DISPATCHED
        shipment.order.save(update_fields=["status"])
    return shipment


@transaction.atomic
def deliver_shipment(shipment):
    shipment = Shipment.objects.select_for_update().get(pk=shipment.pk)
    if shipment.status == Shipment.Status.DELIVERED:
        raise ValueError("El despacho ya fue entregado.")
    shipment.status = Shipment.Status.DELIVERED
    shipment.delivered_date = timezone.localdate()
    shipment.save(update_fields=["status", "delivered_date"])
    shipment.order.status = CustomerOrder.Status.DELIVERED
    shipment.order.save(update_fields=["status"])
    for line in shipment.order.lines.select_related("product"):
        stock = FinishedGoodsStock.objects.select_for_update().get(
            warehouse=shipment.warehouse,
            product=line.product,
        )
        stock.quantity_committed -= line.quantity
        if stock.quantity_committed < 0:
            stock.quantity_committed = 0
        stock.save(update_fields=["quantity_committed"])
    return shipment
