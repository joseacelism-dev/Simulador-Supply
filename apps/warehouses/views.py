from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import FinishedGoodsStockForm, WarehouseForm
from .models import FinishedGoodsStock, Warehouse
from .services import upsert_finished_goods_stock


class WarehouseListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "warehouses/warehouse_list.html"
    context_object_name = "warehouses"

    def get_queryset(self):
        return Warehouse.objects.filter(company__owner=self.request.user).select_related("company")


class WarehouseCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "warehouses/warehouse_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = WarehouseForm()
        return context

    def post(self, request, *args, **kwargs):
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.company = self.company
            warehouse.save()
            messages.success(request, "Almacen creado correctamente.")
            return redirect("warehouses:list")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class FinishedGoodsStockListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "warehouses/finished_stock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        return FinishedGoodsStock.objects.filter(warehouse__company__owner=self.request.user).select_related("warehouse", "product")


class FinishedGoodsStockCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "warehouses/finished_stock_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = FinishedGoodsStockForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = FinishedGoodsStockForm(request.POST, company=self.company)
        if form.is_valid():
            upsert_finished_goods_stock(self.company, form)
            messages.success(request, "Stock terminado actualizado correctamente.")
            return redirect("warehouses:stock_list")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

