from django.urls import path

from .views import DashboardView, SimulationComparisonView


app_name = "reports"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("comparar-simulaciones/", SimulationComparisonView.as_view(), name="compare_simulations"),
]

