from django import forms

from .models import CustomerOrder, CustomerOrderLine


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ("code", "customer", "priority", "promised_date")
        labels = {"code": "Codigo", "customer": "Cliente", "priority": "Prioridad", "promised_date": "Fecha prometida"}
        widgets = {"promised_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["customer"].queryset = company.customers.all()


class CustomerOrderLineForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderLine
        fields = ("product", "quantity", "unit_price")
        labels = {"product": "Producto", "quantity": "Cantidad", "unit_price": "Precio unitario"}

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["product"].queryset = company.products.all()

    def clean_quantity(self):
        value = self.cleaned_data["quantity"]
        if value <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return value

