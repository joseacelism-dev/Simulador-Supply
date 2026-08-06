from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import CustomerComplaintForm, NonConformanceForm, QualityInspectionForm
from .models import CustomerComplaint, QualityInspection
from .services import create_customer_complaint, create_quality_inspection


class QualityInspectionListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "quality/inspection_list.html"
    context_object_name = "inspections"

    def get_queryset(self):
        return QualityInspection.objects.filter(company__owner=self.request.user).select_related("company", "product")


class QualityInspectionCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "quality/inspection_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["inspection_form"] = QualityInspectionForm(company=self.company)
        context["nonconformance_form"] = NonConformanceForm()
        return context

    def post(self, request, *args, **kwargs):
        inspection_form = QualityInspectionForm(request.POST, company=self.company)
        nonconformance_form = NonConformanceForm(request.POST)
        if inspection_form.is_valid() and (nonconformance_form.is_valid() or not request.POST.get("defect_type")):
            inspection = create_quality_inspection(self.company, inspection_form, nonconformance_form)
            messages.success(request, "Inspeccion registrada correctamente.")
            return redirect("quality:inspection_detail", pk=inspection.pk)
        context = self.get_context_data()
        context["inspection_form"] = inspection_form
        context["nonconformance_form"] = nonconformance_form
        return self.render_to_response(context)


class QualityInspectionDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "quality/inspection_detail.html"
    context_object_name = "inspection"

    def get_queryset(self):
        return QualityInspection.objects.filter(company__owner=self.request.user).select_related("company", "product")


class CustomerComplaintListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "quality/complaint_list.html"
    context_object_name = "complaints"

    def get_queryset(self):
        return CustomerComplaint.objects.filter(company__owner=self.request.user).select_related("company", "product", "order")


class CustomerComplaintCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "quality/complaint_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = CustomerComplaintForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerComplaintForm(request.POST, company=self.company)
        if form.is_valid():
            complaint = create_customer_complaint(self.company, form)
            messages.success(request, "Reclamo registrado correctamente.")
            return redirect("quality:complaint_detail", pk=complaint.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class CustomerComplaintDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "quality/complaint_detail.html"
    context_object_name = "complaint"

    def get_queryset(self):
        return CustomerComplaint.objects.filter(company__owner=self.request.user).select_related("company", "product", "order")

