from django.db import transaction

from .models import RiskEvent


@transaction.atomic
def create_risk_event(company, form):
    risk = form.save(commit=False)
    risk.company = company
    risk.save()
    return risk


@transaction.atomic
def create_risk_response(risk_event, form):
    response = form.save(commit=False)
    response.risk_event = risk_event
    response.save()
    risk_event.status = RiskEvent.Status.MITIGATED
    risk_event.save(update_fields=["status"])
    return response

