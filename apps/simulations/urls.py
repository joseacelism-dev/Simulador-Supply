from django.urls import path

from .views import (
    DecisionCreateView,
    ProcessPeriodView,
    SimulationCreateView,
    SimulationDetailView,
    SimulationListView,
    TeacherSimulationListView,
)


app_name = "simulations"

urlpatterns = [
    path("", SimulationListView.as_view(), name="list"),
    path("docente/", TeacherSimulationListView.as_view(), name="teacher_list"),
    path("empresa/<int:company_pk>/crear/", SimulationCreateView.as_view(), name="create_for_company"),
    path("<int:pk>/", SimulationDetailView.as_view(), name="detail"),
    path("<int:pk>/procesar-periodo/", ProcessPeriodView.as_view(), name="process_period"),
    path("<int:simulation_pk>/decisiones/crear/", DecisionCreateView.as_view(), name="decision_create"),
]

