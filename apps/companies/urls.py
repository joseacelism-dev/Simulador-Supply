from django.urls import path

from .views import (
    CompanyCreateView,
    CompanyDetailView,
    CompanyListView,
    TeacherCompanyListView,
)


app_name = "companies"

urlpatterns = [
    path("", CompanyListView.as_view(), name="list"),
    path("crear/", CompanyCreateView.as_view(), name="create"),
    path("docente/", TeacherCompanyListView.as_view(), name="teacher_list"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="detail"),
]

