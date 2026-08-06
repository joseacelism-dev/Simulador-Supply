from django.db import transaction


@transaction.atomic
def create_quality_inspection(company, inspection_form, nonconformance_form=None):
    inspection = inspection_form.save(commit=False)
    inspection.company = company
    inspection.save()
    if nonconformance_form and nonconformance_form.is_valid() and inspection.nonconforming_quantity > 0:
        nonconformance = nonconformance_form.save(commit=False)
        nonconformance.inspection = inspection
        nonconformance.save()
    return inspection


@transaction.atomic
def create_customer_complaint(company, form):
    complaint = form.save(commit=False)
    complaint.company = company
    complaint.save()
    return complaint

