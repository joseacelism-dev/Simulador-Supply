from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import SupplierForm
from .models import Supplier


class SupplierCreateView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "catalogs/supplier_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        return context

    def get_success_url(self):
        return reverse("companies:detail", args=[self.company.pk])

