from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import ProductForm, RawMaterialForm
from .models import Product, RawMaterial


class CompanyCatalogCreateMixin(LoginRequiredMixin, StudentRequiredMixin, CreateView):
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


class ProductCreateView(CompanyCatalogCreateMixin):
    model = Product
    form_class = ProductForm
    template_name = "catalogs/product_form.html"


class RawMaterialCreateView(CompanyCatalogCreateMixin):
    model = RawMaterial
    form_class = RawMaterialForm
    template_name = "catalogs/raw_material_form.html"

