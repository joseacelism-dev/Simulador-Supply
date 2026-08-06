from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.accounts.views import StudentRequiredMixin
from apps.companies.views import get_student_company_or_404

from .forms import CarrierForm, RouteForm, ShipmentForm
from .models import Carrier, Route, Shipment
from .services import create_shipment, deliver_shipment


class CarrierCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "distribution/carrier_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = CarrierForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CarrierForm(request.POST)
        if form.is_valid():
            carrier = form.save(commit=False)
            carrier.company = self.company
            carrier.save()
            messages.success(request, "Transportador creado correctamente.")
            return redirect("distribution:carrier_list")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class CarrierListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "distribution/carrier_list.html"
    context_object_name = "carriers"

    def get_queryset(self):
        return Carrier.objects.filter(company__owner=self.request.user)


class RouteCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "distribution/route_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = RouteForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.company = self.company
            route.save()
            messages.success(request, "Ruta creada correctamente.")
            return redirect("distribution:route_list")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class RouteListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "distribution/route_list.html"
    context_object_name = "routes"

    def get_queryset(self):
        return Route.objects.filter(company__owner=self.request.user)


class ShipmentListView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = "distribution/shipment_list.html"
    context_object_name = "shipments"

    def get_queryset(self):
        return Shipment.objects.filter(company__owner=self.request.user).select_related("order", "carrier", "route", "warehouse")


class ShipmentCreateView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "distribution/shipment_form.html"
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = get_student_company_or_404(request.user, kwargs["company_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.company
        context["form"] = ShipmentForm(company=self.company)
        return context

    def post(self, request, *args, **kwargs):
        form = ShipmentForm(request.POST, company=self.company)
        if form.is_valid():
            try:
                shipment = create_shipment(self.company, form)
            except ValueError as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, "Despacho creado correctamente.")
                return redirect("distribution:shipment_detail", pk=shipment.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class ShipmentDetailView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    template_name = "distribution/shipment_detail.html"
    context_object_name = "shipment"

    def get_queryset(self):
        return Shipment.objects.filter(company__owner=self.request.user).select_related("order", "carrier", "route", "warehouse")


class DeliverShipmentView(LoginRequiredMixin, StudentRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, pk=kwargs["pk"], company__owner=request.user)
        try:
            deliver_shipment(shipment)
            messages.success(request, "Despacho marcado como entregado.")
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect("distribution:shipment_detail", pk=shipment.pk)

