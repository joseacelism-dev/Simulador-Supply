import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .models import Indicator
from .services import generate_company_indicators


class IndicatorListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "indicators/indicator_list.html"
    context_object_name = "indicators"

    def get_queryset(self):
        return Indicator.objects.filter(company__owner=self.request.user).select_related("company", "simulation", "period")


class GenerateIndicatorsView(LoginRequiredMixin, StudentRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        company = get_student_company_or_404(request.user, kwargs["company_pk"])
        generate_company_indicators(company)
        messages.success(request, "Indicadores generados correctamente.")
        return redirect("indicators:list")


class IndicatorCSVExportView(LoginRequiredMixin, StudentRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="indicadores.csv"'
        writer = csv.writer(response)
        writer.writerow(["empresa", "indicador", "formula", "resultado", "unidad", "meta", "estado", "semaforo", "interpretacion", "recomendacion"])
        indicators = Indicator.objects.filter(company__owner=request.user).select_related("company")
        for indicator in indicators:
            writer.writerow([
                indicator.company.name,
                indicator.name,
                indicator.formula,
                indicator.result,
                indicator.unit,
                indicator.target,
                indicator.get_status_display(),
                indicator.get_traffic_light_display(),
                indicator.interpretation,
                indicator.recommendation,
            ])
        return response

