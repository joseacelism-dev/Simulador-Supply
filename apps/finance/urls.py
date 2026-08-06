from django.urls import path

from .views import FinancialSnapshotListView, FinancialTransactionCreateView, FinancialTransactionListView


app_name = "finance"

urlpatterns = [
    path("transacciones/", FinancialTransactionListView.as_view(), name="transaction_list"),
    path("empresa/<int:company_pk>/transacciones/crear/", FinancialTransactionCreateView.as_view(), name="transaction_create_for_company"),
    path("resumenes/", FinancialSnapshotListView.as_view(), name="snapshot_list"),
]

