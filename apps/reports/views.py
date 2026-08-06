from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.views import StudentRequiredMixin

from .services import build_student_dashboard, compare_simulations


class DashboardView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "reports/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(build_student_dashboard(self.request.user))
        return context


class SimulationComparisonView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "reports/simulation_comparison.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = compare_simulations(self.request.user)
        return context

