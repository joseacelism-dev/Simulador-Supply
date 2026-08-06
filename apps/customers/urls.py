from django.urls import path

from .views import CustomerCreateView


app_name = "customers"

urlpatterns = [
    path("empresa/<int:company_pk>/crear/", CustomerCreateView.as_view(), name="create"),
]

