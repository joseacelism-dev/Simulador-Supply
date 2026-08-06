from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from apps.accounts.views import StudentRequiredMixin, TeacherRequiredMixin

from .forms import CompanyForm
from .models import Company


class StudentCompanyQuerysetMixin(LoginRequiredMixin, StudentRequiredMixin):
    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user).select_related("company_type")


class CompanyListView(StudentCompanyQuerysetMixin, ListView):
    template_name = "companies/company_list.html"
    context_object_name = "companies"


class CompanyCreateView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_url = reverse_lazy("companies:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanyDetailView(StudentCompanyQuerysetMixin, DetailView):
    template_name = "companies/company_detail.html"
    context_object_name = "company"


class TeacherCompanyListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    queryset = Company.objects.select_related("owner", "company_type")
    template_name = "companies/teacher_company_list.html"
    context_object_name = "companies"


def get_student_company_or_404(user, pk):
    return get_object_or_404(Company, pk=pk, owner=user)

