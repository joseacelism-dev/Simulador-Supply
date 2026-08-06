from django import forms

from .models import FinancialTransaction


class FinancialTransactionForm(forms.ModelForm):
    class Meta:
        model = FinancialTransaction
        fields = ("category", "description", "amount", "transaction_date")
        labels = {
            "category": "Categoria",
            "description": "Descripcion",
            "amount": "Valor",
            "transaction_date": "Fecha",
        }
        widgets = {"transaction_date": forms.DateInput(attrs={"type": "date"})}

    def clean_amount(self):
        value = self.cleaned_data["amount"]
        if value < 0:
            raise forms.ValidationError("El valor no puede ser negativo.")
        return value

