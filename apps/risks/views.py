from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import RiskEventForm, RiskResponseForm
from .models import RiskEvent
from .services import create_risk_event, create_risk_response


class RiskEventListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "risks/risk_list.html"
    context_object_name = "risks"

    def get_queryset(self):
        return RiskEvent.objects.filter(company__owner=self.request.user).select_related("company")


class RiskEventCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "risks/risk_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = RiskEventForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RiskEventForm(request.POST)
        if form.is_valid():
            risk = create_risk_event(self.company, form)
            messages.success(request, "Riesgo registrado correctamente.")
            return redirect("risks:detail", pk=risk.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class RiskEventDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "risks/risk_detail.html"
    context_object_name = "risk"

    def get_queryset(self):
        return RiskEvent.objects.filter(company__owner=self.request.user).select_related("company")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["response_form"] = RiskResponseForm()
        return context


class RiskResponseCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        risk = get_object_or_404(RiskEvent, pk=kwargs["pk"], company__owner=request.user)
        form = RiskResponseForm(request.POST)
        if form.is_valid():
            create_risk_response(risk, form)
            messages.success(request, "Respuesta de riesgo registrada.")
        else:
            messages.error(request, "No se pudo registrar la respuesta.")
        return redirect("risks:detail", pk=risk.pk)

