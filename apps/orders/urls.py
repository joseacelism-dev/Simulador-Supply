from django.urls import path

from .views import CustomerOrderCreateView, CustomerOrderDetailView, CustomerOrderListView


app_name = "orders"

urlpatterns = [
    path("", CustomerOrderListView.as_view(), name="list"),
    path("empresa/<int:company_pk>/crear/", CustomerOrderCreateView.as_view(), name="create_for_company"),
    path("<int:pk>/", CustomerOrderDetailView.as_view(), name="detail"),
]

