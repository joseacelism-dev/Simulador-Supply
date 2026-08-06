from django.urls import path

from .views import SustainabilityRecordCreateView, SustainabilityRecordDetailView, SustainabilityRecordListView


app_name = "sustainability"

urlpatterns = [
    path("", SustainabilityRecordListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/crear/", SustainabilityRecordCreateView.as_view(), name="create_for_company"),
    path("<int:pk>/", SustainabilityRecordDetailView.as_view(), name="detail"),
]

