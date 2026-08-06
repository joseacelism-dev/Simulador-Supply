from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, ListView
from django.views import View

from apps.accounts.views import StudentRequiredMixin, TeacherRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import DecisionForm, SimulationForm
from .models import Decision, Simulation
from .services import can_register_decision, create_simulation, mark_decision_registered, process_current_period


class StudentSimulationQuerysetMixin(LoginRequiredMixin, StudentRequiredMixin):
    def get_queryset(self):
        return (
            Simulation.objects.filter(company__owner=self.request.user)
            .select_related("company", "company__company_type")
            .prefetch_related("periods")
        )


class SimulationListView(StudentSimulationQuerysetMixin, ListView):
    template_name = "simulations/simulation_list.html"
    context_object_name = "simulations"


class SimulationCreateView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    form_class = SimulationForm
    template_name = "simulations/simulation_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = create_simulation(self.company, form)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return reverse("simulations:detail", args=[self.object.pk])


class SimulationDetailView(StudentSimulationQuerysetMixin, DetailView):
    template_name = "simulations/simulation_detail.html"
    context_object_name = "simulation"

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            "periods__decisions",
            "periods__events",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_period"] = self.object.get_current_period()
        context["decision_form"] = DecisionForm()
        return context


class DecisionCreateView(LoginRequiredMixin, StudentRequiredMixin, FormView):
    form_class = DecisionForm
    simulation = None
    period = None

    def dispatch(self, request, *args, **kwargs):
        self.simulation = get_object_or_404(
            Simulation,
            pk=kwargs["simulation_pk"],
            company__owner=request.user,
        )
        self.period = self.simulation.get_current_period()
        if not can_register_decision(self.period):
            return HttpResponseForbidden("El periodo actual no permite nuevas decisiones.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        decision = form.save(commit=False)
        decision.period = self.period
        decision.save()
        mark_decision_registered(self.period)
        messages.success(self.request, "Decision registrada correctamente.")
        return redirect("simulations:detail", pk=self.simulation.pk)


class ProcessPeriodView(LoginRequiredMixin, StudentRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        simulation = get_object_or_404(
            Simulation,
            pk=kwargs["pk"],
            company__owner=request.user,
        )
        try:
            process_current_period(simulation)
            messages.success(request, "Periodo procesado correctamente.")
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect("simulations:detail", pk=simulation.pk)


class TeacherSimulationListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    queryset = Simulation.objects.select_related("company", "company__owner")
    template_name = "simulations/teacher_simulation_list.html"
    context_object_name = "simulations"

