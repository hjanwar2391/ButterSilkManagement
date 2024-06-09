from django import forms
from .models import Staff, Attendance, Cash
from django.contrib.auth.forms import UserCreationForm
from datetime import date


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["staff_id", "name", "phone", "salary"]


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["staff", "status"]


class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = ["staff", "amount", "description"]


class AttendanceFilterForm(forms.Form):
    day = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), initial=date.today
    )


class CashFilterForm(forms.Form):
    day = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), initial=date.today
    )


class StaffIDForm(forms.Form):
    staff_id = forms.IntegerField(label="Staff ID")
    month = forms.DateField(
        label="Month",
        widget=forms.DateInput(attrs={"type": "month"}),
        input_formats=["%Y-%m"],  # This allows the form to accept the YYYY-MM format
    )


class StaffCashForm(forms.Form):
    staff_id = forms.IntegerField(label="Staff ID")
    month = forms.DateField(
        label="Month",
        widget=forms.DateInput(attrs={"type": "month"}),
        input_formats=["%Y-%m"],  # Allow the form to accept YYYY-MM format
    )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
