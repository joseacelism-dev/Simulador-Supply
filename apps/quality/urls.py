from django.urls import path

from .views import (
    CustomerComplaintCreateView,
    CustomerComplaintDetailView,
    CustomerComplaintListView,
    QualityInspectionCreateView,
    QualityInspectionDetailView,
    QualityInspectionListView,
)


app_name = "quality"

urlpatterns = [
    path("inspecciones/", QualityInspectionListView.as_view(), name="inspection_list"),
    path("empresa/<int:company_pk>/inspecciones/crear/", QualityInspectionCreateView.as_view(), name="inspection_create_for_company"),
    path("inspecciones/<int:pk>/", QualityInspectionDetailView.as_view(), name="inspection_detail"),
    path("reclamos/", CustomerComplaintListView.as_view(), name="complaint_list"),
    path("empresa/<int:company_pk>/reclamos/crear/", CustomerComplaintCreateView.as_view(), name="complaint_create_for_company"),
    path("reclamos/<int:pk>/", CustomerComplaintDetailView.as_view(), name="complaint_detail"),
]

