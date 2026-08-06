from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import PurchaseOrderForm, PurchaseOrderLineForm
from .models import PurchaseOrder
from .services import create_purchase_order, receive_purchase_order


class PurchaseOrderListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "purchasing/purchase_order_list.html"
    context_object_name = "purchase_orders"

    def get_queryset(self):
        return PurchaseOrder.objects.filter(company__owner=self.request.user).select_related("company", "supplier")


class PurchaseOrderCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "purchasing/purchase_order_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["order_form"] = PurchaseOrderForm(company=self.company)
        context["line_form"] = PurchaseOrderLineForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        order_form = PurchaseOrderForm(request.POST, company=self.company)
        line_form = PurchaseOrderLineForm(request.POST, company=self.company)
        if order_form.is_valid() and line_form.is_valid():
            order = create_purchase_order(self.company, order_form, line_form)
            messages.success(request, "Orden de compra creada correctamente.")
            return redirect("purchasing:detail", pk=order.pk)
        context = self.get_context_data()
        context["order_form"] = order_form
        context["line_form"] = line_form
        return self.render_to_response(context)


class PurchaseOrderDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "purchasing/purchase_order_detail.html"
    context_object_name = "purchase_order"

    def get_queryset(self):
        return PurchaseOrder.objects.filter(company__owner=self.request.user).select_related("company", "supplier")


class ReceivePurchaseOrderView(LoginRequiredMixin, StudentRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(PurchaseOrder, pk=kwargs["pk"], company__owner=request.user)
        try:
            receive_purchase_order(order)
            messages.success(request, "Orden recibida e inventario actualizado.")
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect("purchasing:detail", pk=order.pk)

