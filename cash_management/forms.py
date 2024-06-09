from django import forms
from .models import CashAdd, CashSpent
from datetime import date


class CashAddForm(forms.ModelForm):
    class Meta:
        model = CashAdd
        fields = ["amount", "description"]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }


class CashSpentForm(forms.ModelForm):
    class Meta:
        model = CashSpent
        fields = ["amount", "description"]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }
        
class MonthlyCashOverViewForm(forms.Form):
    month = forms.DateField(
        label="Month",
        widget=forms.DateInput(attrs={"type": "month"}),
        input_formats=["%Y-%m"],  # This allows the form to accept the YYYY-MM format
    )
    

class CashFilterForm(forms.Form):
    day = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), 
        initial=date.today
    )
