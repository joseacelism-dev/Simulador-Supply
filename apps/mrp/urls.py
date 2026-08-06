from django.urls import path

from .views import MRPPlanCreateView, MRPPlanDetailView, MRPPlanListView


app_name = "mrp"

urlpatterns = [
    path("", MRPPlanListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/crear/", MRPPlanCreateView.as_view(), name="create_for_company"),
    path("<int:pk>/", MRPPlanDetailView.as_view(), name="detail"),
]

