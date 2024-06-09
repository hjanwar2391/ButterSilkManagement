from django import forms
from .models import Store, Product, DailySales, DepositAmount
from datetime import datetime


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "store_id", "address"]


class ProductForm(forms.ModelForm):
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(), label="Store", required=True
    )

    class Meta:
        model = Product
        fields = ["store", "name", "quantity", "invoice_no", "description"]


class DailySalesForm(forms.ModelForm):
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(), label="Store", required=True
    )

    class Meta:
        model = DailySales
        fields = [
            "store",
            "product",
            "sell_amount",
            "sell_quantity_products",
            "sell_due",
            "return_product_quantity",
            "cost_amount",
            "description",
        ]


class DepositAmountForm(forms.ModelForm):
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(), label="Store", required=True
    )

    class Meta:
        model = DepositAmount
        fields = ["store", "amount", "description"]


class StoreIDForm(forms.Form):
    store_id = forms.CharField(label='Enter Store ID', max_length=10)
    def clean_store_id(self):
        store_id = self.cleaned_data['store_id']
        try:
            store = Store.objects.get(store_id=store_id)
        except Store.DoesNotExist:
            raise forms.ValidationError("Invalid Store ID")
        return store_id

class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))


class StoreMonthlyFilterForm(forms.Form):
    store = forms.ModelChoiceField(queryset=Store.objects.all(), required=True)
    month = forms.DateField(
        label="Month",
        widget=forms.DateInput(attrs={"type": "month"}),
        input_formats=["%Y-%m"],  # This allows the form to accept the YYYY-MM format
    )


# product sell and return
class StoreMonthForm(forms.Form):
    store_id = forms.IntegerField(label="Store ID")
    month = forms.DateField(
        label="Month",
        widget=forms.DateInput(attrs={"type": "month", "format": "%Y-%m"}),
        initial=datetime.now().strftime("%Y-%m"),
        input_formats=["%Y-%m"],
    )
