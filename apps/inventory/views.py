from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import InventoryPolicyForm
from .models import InventoryItem, InventoryPolicy
from .services import get_inventory_alerts


class InventoryListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "inventory/inventory_list.html"
    context_object_name = "inventory_items"

    def get_queryset(self):
        return InventoryItem.objects.filter(company__owner=self.request.user).select_related("company", "raw_material")


class InventoryPolicyCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "inventory/inventory_policy_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = InventoryPolicyForm(company=self.company)
        context["policies"] = self.company.inventory_policies.select_related("raw_material")
        context["alerts"] = get_inventory_alerts(self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = InventoryPolicyForm(request.POST, company=self.company)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.company = self.company
            policy.save()
            messages.success(request, "Politica de inventario guardada correctamente.")
            return redirect("inventory:policy_create_for_company", company_pk=self.company.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class InventoryPolicyListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "inventory/inventory_policy_list.html"
    context_object_name = "policies"

    def get_queryset(self):
        return InventoryPolicy.objects.filter(company__owner=self.request.user).select_related("company", "raw_material")

