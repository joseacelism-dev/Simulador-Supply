from django.db import transaction

from .models import ReturnRequest


@transaction.atomic
def create_return_request(company, return_form, line_form):
    return_request = return_form.save(commit=False)
    return_request.company = company
    return_request.save()
    line = line_form.save(commit=False)
    line.return_request = return_request
    line.save()
    return return_request


@transaction.atomic
def inspect_return(return_request, inspection_form):
    inspection = inspection_form.save(commit=False)
    inspection.return_request = return_request
    inspection.save()
    return_request.status = ReturnRequest.Status.INSPECTED
    return_request.save(update_fields=["status"])
    return inspection


@transaction.atomic
def decide_disposition(return_request, form):
    disposition = form.save(commit=False)
    disposition.return_request = return_request
    disposition.save()
    return_request.status = ReturnRequest.Status.DISPOSED
    return_request.save(update_fields=["status"])
    return disposition

