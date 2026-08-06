from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import DispositionDecisionForm, ReturnInspectionForm, ReturnLineForm, ReturnRequestForm
from .models import ReturnRequest
from .services import create_return_request, decide_disposition, inspect_return


class ReturnRequestListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "reverse_logistics/return_list.html"
    context_object_name = "returns"

    def get_queryset(self):
        return ReturnRequest.objects.filter(company__owner=self.request.user).select_related("company", "order")


class ReturnRequestCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "reverse_logistics/return_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["return_form"] = ReturnRequestForm(company=self.company)
        context["line_form"] = ReturnLineForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        return_form = ReturnRequestForm(request.POST, company=self.company)
        line_form = ReturnLineForm(request.POST, company=self.company)
        if return_form.is_valid() and line_form.is_valid():
            return_request = create_return_request(self.company, return_form, line_form)
            messages.success(request, "Solicitud de devolucion creada correctamente.")
            return redirect("reverse_logistics:return_detail", pk=return_request.pk)
        context = self.get_context_data()
        context["return_form"] = return_form
        context["line_form"] = line_form
        return self.render_to_response(context)


class ReturnRequestDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "reverse_logistics/return_detail.html"
    context_object_name = "return_request"

    def get_queryset(self):
        return ReturnRequest.objects.filter(company__owner=self.request.user).select_related("company", "order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inspection_form"] = ReturnInspectionForm()
        context["disposition_form"] = DispositionDecisionForm()
        return context


class ReturnInspectionCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        return_request = get_object_or_404(ReturnRequest, pk=kwargs["pk"], company__owner=request.user)
        form = ReturnInspectionForm(request.POST)
        if form.is_valid():
            inspect_return(return_request, form)
            messages.success(request, "Inspeccion de devolucion registrada.")
        else:
            messages.error(request, "No se pudo registrar la inspeccion.")
        return redirect("reverse_logistics:return_detail", pk=return_request.pk)


class DispositionDecisionCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        return_request = get_object_or_404(ReturnRequest, pk=kwargs["pk"], company__owner=request.user)
        form = DispositionDecisionForm(request.POST)
        if form.is_valid():
            decide_disposition(return_request, form)
            messages.success(request, "Decision de disposicion registrada.")
        else:
            messages.error(request, "No se pudo registrar la disposicion.")
        return redirect("reverse_logistics:return_detail", pk=return_request.pk)

