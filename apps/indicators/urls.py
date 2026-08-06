from django.urls import path

from .views import GenerateIndicatorsView, IndicatorCSVExportView, IndicatorListView


app_name = "indicators"

urlpatterns = [
    path("", IndicatorListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/generar/", GenerateIndicatorsView.as_view(), name="generate_for_company"),
    path("exportar-csv/", IndicatorCSVExportView.as_view(), name="export_csv"),
]

