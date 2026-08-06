from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.inventory.services import get_inventory_alerts
from apps.purchasing.models import PurchaseOrder
from apps.production.models import ProductionOrder
from apps.production.services import get_material_shortages

from .models import Decision, PeriodResult, Simulation, SimulationEvent, SimulationPeriod


def create_initial_period(simulation):
    return SimulationPeriod.objects.create(
        simulation=simulation,
        number=1,
        status=SimulationPeriod.Status.OPEN,
    )


def create_simulation(company, form):
    simulation = form.save(commit=False)
    simulation.company = company
    simulation.status = Simulation.Status.PERIOD_OPEN
    simulation.current_period_number = 1
    simulation.save()
    create_initial_period(simulation)
    return simulation


@transaction.atomic
def process_current_period(simulation):
    simulation = Simulation.objects.select_for_update().get(pk=simulation.pk)
    period = simulation.get_current_period()
    if period is None:
        raise ValueError("La simulacion no tiene un periodo actual.")
    if not period.is_open:
        raise ValueError("El periodo actual no esta abierto.")

    period.status = SimulationPeriod.Status.PROCESSING
    period.save(update_fields=["status"])
    simulation.status = Simulation.Status.PROCESSING
    simulation.save(update_fields=["status", "updated_at"])

    decisions = period.decisions.all()
    decisions.update(locked=True)

    company = simulation.company
    product_count = company.products.count()
    raw_material_count = company.raw_materials.count()
    supplier_count = company.suppliers.count()
    customer_count = company.customers.count()
    decision_count = decisions.count()
    pending_purchase_count = PurchaseOrder.objects.filter(
        company=company,
        status__in=[
            PurchaseOrder.Status.ORDERED,
            PurchaseOrder.Status.PARTIALLY_RECEIVED,
        ],
    ).count()
    inventory_alerts = get_inventory_alerts(company)
    open_production_orders = ProductionOrder.objects.filter(
        company=company,
        status__in=[
            ProductionOrder.Status.PLANNED,
            ProductionOrder.Status.RELEASED,
            ProductionOrder.Status.WAITING,
            ProductionOrder.Status.IN_PROCESS,
        ],
    )
    production_shortages = []
    for order in open_production_orders:
        production_shortages.extend(get_material_shortages(order))

    operational_score = _calculate_operational_score(
        product_count=product_count,
        raw_material_count=raw_material_count,
        supplier_count=supplier_count,
        customer_count=customer_count,
        decision_count=decision_count,
    )

    PeriodResult.objects.update_or_create(
        period=period,
        defaults={
            "available_capital": company.initial_capital,
            "product_count": product_count,
            "raw_material_count": raw_material_count,
            "supplier_count": supplier_count,
            "customer_count": customer_count,
            "decision_count": decision_count,
            "operational_score": operational_score,
            "summary": _build_summary(
                decision_count=decision_count,
                product_count=product_count,
                raw_material_count=raw_material_count,
                supplier_count=supplier_count,
                customer_count=customer_count,
            ),
        },
    )

    _create_period_events(
        period,
        decision_count,
        supplier_count,
        customer_count,
        pending_purchase_count,
        inventory_alerts,
        open_production_orders.count(),
        production_shortages,
    )

    period.status = SimulationPeriod.Status.CLOSED
    period.closed_at = timezone.now()
    period.save(update_fields=["status", "closed_at"])

    if period.number >= simulation.total_periods:
        simulation.status = Simulation.Status.FINISHED
    else:
        simulation.current_period_number = period.number + 1
        simulation.status = Simulation.Status.PERIOD_OPEN
        SimulationPeriod.objects.create(
            simulation=simulation,
            number=simulation.current_period_number,
            status=SimulationPeriod.Status.OPEN,
        )
    simulation.save(update_fields=["status", "current_period_number", "updated_at"])
    return period


def mark_decision_registered(period):
    if period.status == SimulationPeriod.Status.OPEN:
        period.status = SimulationPeriod.Status.DECISIONS_REGISTERED
        period.save(update_fields=["status"])
        simulation = period.simulation
        simulation.status = Simulation.Status.DECISIONS_REGISTERED
        simulation.save(update_fields=["status", "updated_at"])


def can_register_decision(period):
    return period is not None and period.is_open


def _calculate_operational_score(
    product_count,
    raw_material_count,
    supplier_count,
    customer_count,
    decision_count,
):
    base = Decimal("40")
    catalog_points = min(product_count, 5) * 4
    catalog_points += min(raw_material_count, 5) * 3
    catalog_points += min(supplier_count, 3) * 5
    catalog_points += min(customer_count, 3) * 4
    decision_points = min(decision_count, 5) * 2
    score = base + Decimal(catalog_points + decision_points)
    return min(score, Decimal("100"))


def _build_summary(
    decision_count,
    product_count,
    raw_material_count,
    supplier_count,
    customer_count,
):
    return (
        f"Periodo procesado con {decision_count} decisiones. "
        f"Catalogos disponibles: {product_count} productos, "
        f"{raw_material_count} materias primas, {supplier_count} proveedores "
        f"y {customer_count} clientes."
    )


def _create_period_events(
    period,
    decision_count,
    supplier_count,
    customer_count,
    pending_purchase_count,
    inventory_alerts,
    open_production_count,
    production_shortages,
):
    SimulationEvent.objects.create(
        period=period,
        name="Periodo procesado",
        description="El motor proceso decisiones, catalogos y resultados basicos del periodo.",
        severity=SimulationEvent.Severity.INFO,
    )

    if decision_count == 0:
        SimulationEvent.objects.create(
            period=period,
            name="Periodo sin decisiones",
            description="No se registraron decisiones antes del cierre del periodo.",
            severity=SimulationEvent.Severity.PREVENTIVE,
        )

    if supplier_count == 0:
        SimulationEvent.objects.create(
            period=period,
            name="Sin proveedores registrados",
            description="La empresa no tiene proveedores. En fases futuras esto limitara compras y abastecimiento.",
            severity=SimulationEvent.Severity.IMPORTANT,
        )

    if customer_count == 0:
        SimulationEvent.objects.create(
            period=period,
            name="Sin clientes registrados",
            description="La empresa no tiene clientes. En fases futuras esto limitara demanda y pedidos.",
            severity=SimulationEvent.Severity.IMPORTANT,
        )

    if pending_purchase_count:
        SimulationEvent.objects.create(
            period=period,
            name="Compras pendientes",
            description=f"Existen {pending_purchase_count} ordenes de compra pendientes de recepcion.",
            severity=SimulationEvent.Severity.PREVENTIVE,
        )

    for alert in inventory_alerts:
        SimulationEvent.objects.create(
            period=period,
            name="Inventario bajo",
            description=(
                f"{alert['material'].name}: disponible {alert['available']} "
                f"frente a punto de reorden {alert['reorder_point']}."
            ),
            severity=SimulationEvent.Severity.IMPORTANT,
        )

    if open_production_count:
        SimulationEvent.objects.create(
            period=period,
            name="Ordenes de produccion abiertas",
            description=f"Existen {open_production_count} ordenes de produccion sin finalizar.",
            severity=SimulationEvent.Severity.PREVENTIVE,
        )

    for shortage in production_shortages:
        SimulationEvent.objects.create(
            period=period,
            name="Faltante para produccion",
            description=(
                f"{shortage['raw_material'].name}: requerido {shortage['required']}, "
                f"disponible {shortage['available']}."
            ),
            severity=SimulationEvent.Severity.CRITICAL,
        )
