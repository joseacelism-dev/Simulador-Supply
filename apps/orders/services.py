from django.db import transaction


@transaction.atomic
def create_customer_order(company, order_form, line_form):
    order = order_form.save(commit=False)
    order.company = company
    order.save()
    line = line_form.save(commit=False)
    line.order = order
    line.save()
    return order

