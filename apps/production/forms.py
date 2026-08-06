from django import forms

from .models import BillOfMaterials, BillOfMaterialsLine, ProductionOrder, WorkCenter


class BillOfMaterialsForm(forms.ModelForm):
    class Meta:
        model = BillOfMaterials
        fields = ("product", "version", "is_active")
        labels = {"product": "Producto", "version": "Version", "is_active": "Activa"}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["product"].queryset = company.products.all()


class BillOfMaterialsLineForm(forms.ModelForm):
    class Meta:
        model = BillOfMaterialsLine
        fields = ("raw_material", "quantity_per_unit", "scrap_percentage")
        labels = {
            "raw_material": "Materia prima",
            "quantity_per_unit": "Cantidad por unidad",
            "scrap_percentage": "Merma porcentual",
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["raw_material"].queryset = company.raw_materials.all()

    def clean_quantity_per_unit(self):
        value = self.cleaned_data["quantity_per_unit"]
        if value <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return value


class ProductionOrderForm(forms.ModelForm):
    class Meta:
        model = ProductionOrder
        fields = ("code", "bom", "quantity", "strategy", "planned_start_date", "planned_end_date")
        labels = {
            "code": "Codigo",
            "bom": "BOM",
            "quantity": "Cantidad",
            "strategy": "Estrategia",
            "planned_start_date": "Inicio planificado",
            "planned_end_date": "Fin planificado",
        }
        widgets = {
            "planned_start_date": forms.DateInput(attrs={"type": "date"}),
            "planned_end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["bom"].queryset = company.boms.filter(is_active=True)

    def clean_quantity(self):
        value = self.cleaned_data["quantity"]
        if value <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return value


class WorkCenterForm(forms.ModelForm):
    class Meta:
        model = WorkCenter
        fields = ("name", "daily_capacity", "labor_cost_per_hour")
        labels = {
            "name": "Nombre",
            "daily_capacity": "Capacidad diaria",
            "labor_cost_per_hour": "Costo hora mano de obra",
        }

