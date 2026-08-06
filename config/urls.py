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
    path("simulaciones/", include("apps.simulations.urls")),
    path("compras/", include("apps.purchasing.urls")),
    path("inventarios/", include("apps.inventory.urls")),
    path("produccion/", include("apps.production.urls")),
    path("mrp/", include("apps.mrp.urls")),
    path("almacenes/", include("apps.warehouses.urls")),
    path("pedidos/", include("apps.orders.urls")),
    path("distribucion/", include("apps.distribution.urls")),
    path("calidad/", include("apps.quality.urls")),
    path("logistica-inversa/", include("apps.reverse_logistics.urls")),
    path("finanzas/", include("apps.finance.urls")),
    path("riesgos/", include("apps.risks.urls")),
    path("sostenibilidad/", include("apps.sustainability.urls")),
]
