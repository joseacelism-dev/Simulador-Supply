from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import FinancialTransactionForm
from .models import FinancialSnapshot, FinancialTransaction
from .services import calculate_financial_summary, create_financial_snapshot, create_financial_transaction


class FinancialTransactionListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "finance/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return FinancialTransaction.objects.filter(company__owner=self.request.user).select_related("company")


class FinancialTransactionCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "finance/transaction_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = FinancialTransactionForm()
        context["summary"] = calculate_financial_summary(self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = FinancialTransactionForm(request.POST)
        if form.is_valid():
            create_financial_transaction(self.company, form)
            create_financial_snapshot(self.company, name="Resumen automatico")
            messages.success(request, "Transaccion financiera registrada.")
            return redirect("finance:snapshot_list")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class FinancialSnapshotListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "finance/snapshot_list.html"
    context_object_name = "snapshots"

    def get_queryset(self):
        return FinancialSnapshot.objects.filter(company__owner=self.request.user).select_related("company")

