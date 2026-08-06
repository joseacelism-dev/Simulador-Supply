from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import CustomerOrderForm, CustomerOrderLineForm
from .models import CustomerOrder
from .services import create_customer_order


class CustomerOrderListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return CustomerOrder.objects.filter(company__owner=self.request.user).select_related("company", "customer")


class CustomerOrderCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "orders/order_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["order_form"] = CustomerOrderForm(company=self.company)
        context["line_form"] = CustomerOrderLineForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        order_form = CustomerOrderForm(request.POST, company=self.company)
        line_form = CustomerOrderLineForm(request.POST, company=self.company)
        if order_form.is_valid() and line_form.is_valid():
            order = create_customer_order(self.company, order_form, line_form)
            messages.success(request, "Pedido creado correctamente.")
            return redirect("orders:detail", pk=order.pk)
        context = self.get_context_data()
        context["order_form"] = order_form
        context["line_form"] = line_form
        return self.render_to_response(context)


class CustomerOrderDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return CustomerOrder.objects.filter(company__owner=self.request.user).select_related("company", "customer")

