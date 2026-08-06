from django.urls import path

from .views import (
    DispositionDecisionCreateView,
    ReturnInspectionCreateView,
    ReturnRequestCreateView,
    ReturnRequestDetailView,
    ReturnRequestListView,
)


app_name = "reverse_logistics"

urlpatterns = [
    path("", ReturnRequestListView.as_view(), name="return_list"),
    path("empresa/<int:company_pk>/crear/", ReturnRequestCreateView.as_view(), name="return_create_for_company"),
    path("<int:pk>/", ReturnRequestDetailView.as_view(), name="return_detail"),
    path("<int:pk>/inspeccionar/", ReturnInspectionCreateView.as_view(), name="return_inspect"),
    path("<int:pk>/disponer/", DispositionDecisionCreateView.as_view(), name="return_dispose"),
]

