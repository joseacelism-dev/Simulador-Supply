from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import MRPPlanForm
from .models import MRPPlan
from .services import create_mrp_plan


class MRPPlanListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "mrp/mrp_plan_list.html"
    context_object_name = "plans"

    def get_queryset(self):
        return MRPPlan.objects.filter(company__owner=self.request.user).select_related("company", "product")


class MRPPlanCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "mrp/mrp_plan_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = MRPPlanForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = MRPPlanForm(request.POST, company=self.company)
        if form.is_valid():
            try:
                plan = create_mrp_plan(self.company, form)
            except ValueError as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, "Plan MRP generado correctamente.")
                return redirect("mrp:detail", pk=plan.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class MRPPlanDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "mrp/mrp_plan_detail.html"
    context_object_name = "plan"

    def get_queryset(self):
        return MRPPlan.objects.filter(company__owner=self.request.user).select_related("company", "product").prefetch_related("lines")

