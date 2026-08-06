from django.urls import path

from .views import RiskEventCreateView, RiskEventDetailView, RiskEventListView, RiskResponseCreateView


app_name = "risks"

urlpatterns = [
    path("", RiskEventListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/crear/", RiskEventCreateView.as_view(), name="create_for_company"),
    path("<int:pk>/", RiskEventDetailView.as_view(), name="detail"),
    path("<int:pk>/responder/", RiskResponseCreateView.as_view(), name="response_create"),
]
