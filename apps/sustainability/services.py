from django.db import transaction


@transaction.atomic
def create_sustainability_record(company, form):
    record = form.save(commit=False)
    record.company = company
    record.save()
    return record

