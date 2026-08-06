from decimal import Decimal

from django.db import transaction

from apps.finance.services import calculate_financial_summary
from apps.orders.models import CustomerOrder
from apps.quality.models import QualityInspection
from apps.reverse_logistics.models import ReturnRequest
from apps.risks.models import RiskEvent
from apps.sustainability.models import SustainabilityRecord

from .models import Indicator


@transaction.atomic
def generate_company_indicators(company, simulation=None, period=None):
    Indicator.objects.filter(company=company, simulation=simulation, period=period).delete()
    specs = _build_indicator_specs(company, simulation, period)
    indicators = []
    for spec in specs:
        indicators.append(Indicator.objects.create(company=company, simulation=simulation, period=period, **spec))
    return indicators


def _build_indicator_specs(company, simulation=None, period=None):
    orders = company.customer_orders.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status=CustomerOrder.Status.DELIVERED).count()
    service_level = _percentage(delivered_orders, total_orders)

    returns = company.return_requests.count()
    return_rate = _percentage(returns, total_orders)

    inspected = Decimal("0")
    nonconforming = Decimal("0")
    for inspection in company.quality_inspections.all():
        inspected += Decimal(inspection.inspected_quantity)
        nonconforming += Decimal(inspection.nonconforming_quantity)
    defect_rate = _percentage(nonconforming, inspected)

    financial = calculate_financial_summary(company)
    open_risks = company.risk_events.filter(status=RiskEvent.Status.OPEN).count()
    latest_sustainability = SustainabilityRecord.objects.filter(company=company).first()
    emissions = Decimal("0")
    recovered_waste = Decimal("0")
    if latest_sustainability:
        emissions = latest_sustainability.total_emissions
        recovered_waste = latest_sustainability.recovered_waste_percentage

    operational_score = Decimal("0")
    if period and hasattr(period, "result"):
        operational_score = Decimal(period.result.operational_score)

    return [
        _indicator("service_level", "Nivel de servicio", "pedidos entregados / pedidos totales * 100", service_level, "%", Decimal("95")),
        _indicator("delivered_rate", "Tasa de pedidos entregados", "pedidos entregados / pedidos totales * 100", service_level, "%", Decimal("95")),
        _indicator("return_rate", "Tasa de devoluciones", "devoluciones / pedidos totales * 100", return_rate, "%", Decimal("5"), lower_is_better=True),
        _indicator("defect_rate", "Tasa de defectos", "unidades no conformes / unidades inspeccionadas * 100", defect_rate, "%", Decimal("3"), lower_is_better=True),
        _indicator("operating_margin", "Margen operativo", "utilidad / ingresos * 100", financial["margin"], "%", Decimal("15")),
        _indicator("cash_flow", "Flujo de caja", "capital inicial + ingresos - costos", financial["cash_flow"], company.currency, Decimal("0")),
        _indicator("open_risks", "Riesgos abiertos", "conteo de riesgos abiertos", Decimal(open_risks), "riesgos", Decimal("0"), lower_is_better=True),
        _indicator("transport_emissions", "Emisiones de transporte", "kg CO2e registrados", emissions, "kg CO2e", Decimal("0"), lower_is_better=True),
        _indicator("recovered_waste", "Residuos recuperados", "residuos recuperados / residuos generados * 100", recovered_waste, "%", Decimal("40")),
        _indicator("operational_score", "Puntaje operacional", "resultado operacional del periodo", operational_score, "pts", Decimal("80")),
    ]


def _percentage(numerator, denominator):
    numerator = Decimal(numerator)
    denominator = Decimal(denominator)
    if denominator <= 0:
        return Decimal("0")
    return (numerator / denominator * Decimal("100")).quantize(Decimal("0.01"))


def _indicator(code, name, formula, result, unit, target, lower_is_better=False):
    status, traffic_light = _status(result, target, lower_is_better)
    return {
        "code": code,
        "name": name,
        "formula": formula,
        "result": result,
        "unit": unit,
        "target": target,
        "status": status,
        "traffic_light": traffic_light,
        "interpretation": _interpretation(name, result, unit, status),
        "recommendation": _recommendation(status),
    }


def _status(result, target, lower_is_better):
    if lower_is_better:
        if result <= target:
            return Indicator.Status.GOOD, Indicator.TrafficLight.GREEN
        if result <= target * Decimal("1.5"):
            return Indicator.Status.WARNING, Indicator.TrafficLight.YELLOW
        return Indicator.Status.CRITICAL, Indicator.TrafficLight.RED
    if result >= target:
        return Indicator.Status.GOOD, Indicator.TrafficLight.GREEN
    if result >= target * Decimal("0.8"):
        return Indicator.Status.WARNING, Indicator.TrafficLight.YELLOW
    return Indicator.Status.CRITICAL, Indicator.TrafficLight.RED


def _interpretation(name, result, unit, status):
    return f"{name}: resultado {result} {unit}. Estado {status}."


def _recommendation(status):
    if status == Indicator.Status.GOOD:
        return "Mantener la estrategia actual y monitorear tendencia."
    if status == Indicator.Status.WARNING:
        return "Revisar causas y preparar acciones preventivas."
    return "Priorizar accion correctiva en el siguiente periodo."

