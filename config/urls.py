from django.contrib import admin
from django.urls import include, path
from apps.accounts.views import HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("empresas/", include("apps.companies.urls")),
    path("productos/", include("apps.products.urls")),
    path("proveedores/", include("apps.suppliers.urls")),
    path("clientes/", include("apps.customers.urls")),
]
