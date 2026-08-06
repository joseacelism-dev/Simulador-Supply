from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType
from apps.customers.models import Customer
from apps.orders.models import CustomerOrder
from apps.products.models import Product
from apps.warehouses.models import FinishedGoodsStock, Warehouse

from .models import Carrier, Route, Shipment


class DistributionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        company_type = CompanyType.objects.create(name="Ecommerce", description="Prueba")
        self.company = Company.objects.create(owner=self.user, company_type=company_type, name="Tienda Ana", city="Bogota", target_market="Digital")
        self.customer = Customer.objects.create(company=self.company, name="Cliente Uno", segment="B2C", city="Bogota")
        self.product = Product.objects.create(company=self.company, sku="P-001", name="Producto", sale_price="10000")
        self.order = CustomerOrder.objects.create(company=self.company, customer=self.customer, code="PED-001")
        self.order.lines.create(product=self.product, quantity="4", unit_price="10000")
        self.warehouse = Warehouse.objects.create(company=self.company, name="CEDI", city="Bogota")
        self.carrier = Carrier.objects.create(company=self.company, name="Transportes Uno", cost_per_km="2000")
        self.route = Route.objects.create(company=self.company, name="Bogota norte", origin_city="Bogota", destination_city="Bogota", distance_km="8")

    def test_shipment_discounts_stock(self):
        FinishedGoodsStock.objects.create(warehouse=self.warehouse, product=self.product, quantity_available="10")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("distribution:shipment_create_for_company", args=[self.company.pk]),
            {
                "code": "DES-001",
                "order": self.order.pk,
                "warehouse": self.warehouse.pk,
                "carrier": self.carrier.pk,
                "route": self.route.pk,
            },
        )

        shipment = Shipment.objects.get(code="DES-001")
        stock = FinishedGoodsStock.objects.get(warehouse=self.warehouse, product=self.product)
        self.assertRedirects(response, reverse("distribution:shipment_detail", args=[shipment.pk]))
        self.assertEqual(stock.quantity_available, 6)
        self.assertEqual(stock.quantity_committed, 4)

    def test_shipment_without_stock_sets_order_backorder(self):
        FinishedGoodsStock.objects.create(warehouse=self.warehouse, product=self.product, quantity_available="1")
        self.client.force_login(self.user)

        self.client.post(
            reverse("distribution:shipment_create_for_company", args=[self.company.pk]),
            {
                "code": "DES-002",
                "order": self.order.pk,
                "warehouse": self.warehouse.pk,
                "carrier": self.carrier.pk,
                "route": self.route.pk,
            },
        )

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, CustomerOrder.Status.BACKORDER)
        self.assertFalse(Shipment.objects.filter(code="DES-002").exists())

    def test_deliver_shipment_updates_order_and_committed_stock(self):
        stock = FinishedGoodsStock.objects.create(warehouse=self.warehouse, product=self.product, quantity_available="6", quantity_committed="4")
        shipment = Shipment.objects.create(company=self.company, order=self.order, warehouse=self.warehouse, carrier=self.carrier, route=self.route, code="DES-003")
        self.client.force_login(self.user)

        response = self.client.post(reverse("distribution:shipment_deliver", args=[shipment.pk]))

        shipment.refresh_from_db()
        self.order.refresh_from_db()
        stock.refresh_from_db()
        self.assertRedirects(response, reverse("distribution:shipment_detail", args=[shipment.pk]))
        self.assertEqual(shipment.status, Shipment.Status.DELIVERED)
        self.assertEqual(self.order.status, CustomerOrder.Status.DELIVERED)
        self.assertEqual(stock.quantity_committed, 0)

