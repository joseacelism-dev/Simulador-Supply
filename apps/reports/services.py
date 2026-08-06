from apps.finance.services import calculate_financial_summary
from apps.indicators.models import Indicator
from apps.simulations.models import Simulation


def build_student_dashboard(user):
    companies = user.companies.all()
    company = companies.first()
    if company is None:
        return {"company": None}
    indicators = Indicator.objects.filter(company=company).order_by("name")
    return {
        "company": company,
        "financial": calculate_financial_summary(company),
        "indicators": indicators[:10],
        "simulations": company.simulations.all()[:5],
        "critical_count": indicators.filter(traffic_light=Indicator.TrafficLight.RED).count(),
        "warning_count": indicators.filter(traffic_light=Indicator.TrafficLight.YELLOW).count(),
    }


def compare_simulations(user):
    simulations = Simulation.objects.filter(company__owner=user).prefetch_related("periods__result")[:10]
    rows = []
    for simulation in simulations:
        closed_periods = [period for period in simulation.periods.all() if hasattr(period, "result")]
        average_score = 0
        if closed_periods:
            average_score = sum(period.result.operational_score for period in closed_periods) / len(closed_periods)
        rows.append(
            {
                "simulation": simulation,
                "closed_periods": len(closed_periods),
                "average_score": average_score,
                "status": simulation.get_status_display(),
            }
        )
    return rows

