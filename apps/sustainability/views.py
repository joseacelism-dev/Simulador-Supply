from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import SustainabilityRecordForm
from .models import SustainabilityRecord
from .services import create_sustainability_record


class SustainabilityRecordListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "sustainability/record_list.html"
    context_object_name = "records"

    def get_queryset(self):
        return SustainabilityRecord.objects.filter(company__owner=self.request.user).select_related("company")


class SustainabilityRecordCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "sustainability/record_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = SustainabilityRecordForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SustainabilityRecordForm(request.POST)
        if form.is_valid():
            record = create_sustainability_record(self.company, form)
            messages.success(request, "Registro de sostenibilidad guardado.")
            return redirect("sustainability:detail", pk=record.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class SustainabilityRecordDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "sustainability/record_detail.html"
    context_object_name = "record"

    def get_queryset(self):
        return SustainabilityRecord.objects.filter(company__owner=self.request.user).select_related("company")

