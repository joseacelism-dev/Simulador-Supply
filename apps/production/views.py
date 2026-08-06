from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import BillOfMaterialsForm, BillOfMaterialsLineForm, ProductionOrderForm
from .models import BillOfMaterials, ProductionOrder
from .services import create_bom, create_production_order, get_material_shortages, complete_production_order


class BillOfMaterialsListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "production/bom_list.html"
    context_object_name = "boms"

    def get_queryset(self):
        return BillOfMaterials.objects.filter(company__owner=self.request.user).select_related("company", "product")


class BillOfMaterialsCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "production/bom_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["bom_form"] = BillOfMaterialsForm(company=self.company)
        context["line_form"] = BillOfMaterialsLineForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        bom_form = BillOfMaterialsForm(request.POST, company=self.company)
        line_form = BillOfMaterialsLineForm(request.POST, company=self.company)
        if bom_form.is_valid() and line_form.is_valid():
            bom = create_bom(self.company, bom_form, line_form)
            messages.success(request, "BOM creada correctamente.")
            return redirect("production:bom_detail", pk=bom.pk)
        context = self.get_context_data()
        context["bom_form"] = bom_form
        context["line_form"] = line_form
        return self.render_to_response(context)


class BillOfMaterialsDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "production/bom_detail.html"
    context_object_name = "bom"

    def get_queryset(self):
        return BillOfMaterials.objects.filter(company__owner=self.request.user).select_related("company", "product")


class ProductionOrderListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "production/production_order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return ProductionOrder.objects.filter(company__owner=self.request.user).select_related("company", "bom", "bom__product")


class ProductionOrderCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "production/production_order_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = ProductionOrderForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = ProductionOrderForm(request.POST, company=self.company)
        if form.is_valid():
            order = create_production_order(self.company, form)
            messages.success(request, "Orden de produccion creada correctamente.")
            return redirect("production:order_detail", pk=order.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class ProductionOrderDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "production/production_order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return ProductionOrder.objects.filter(company__owner=self.request.user).select_related("company", "bom", "bom__product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shortages"] = get_material_shortages(self.object)
        return context


class CompleteProductionOrderView(LoginRequiredMixin, StudentRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(ProductionOrder, pk=kwargs["pk"], company__owner=request.user)
        try:
            complete_production_order(order)
            messages.success(request, "Orden completada y materiales consumidos.")
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect("production:order_detail", pk=order.pk)

