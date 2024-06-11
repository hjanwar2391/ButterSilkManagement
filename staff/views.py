from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, Attendance, Cash
from .forms import (
    StaffForm,
    AttendanceForm,
    CashForm,
    StaffIDForm,
    StaffCashForm,
    AttendanceFilterForm,
    CashFilterForm,
    LoginForm,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from calendar import monthrange, FRIDAY
from datetime import timedelta, datetime, date
import math
from django.db import models
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "staff/home.html")


def add_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff added successfully!")
            return redirect("add_staff")
    else:
        form = StaffForm()
    return render(request, "staff/add_staff.html", {"form": form})


def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, "staff/staff_list.html", {"staff_members": staff_members})


def add_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("attendance_list")
    else:
        form = AttendanceForm()
    return render(request, "staff/add_attendance.html", {"form": form})


def attendance_list(request):
    form = AttendanceFilterForm(request.GET or None)
    if form.is_valid():
        day = form.cleaned_data.get("day")
        attendances = Attendance.objects.filter(date=day).order_by("-date")
    else:
        attendances = Attendance.objects.filter(date=date.today()).order_by("-date")

    return render(
        request,
        "staff/attendance_list.html",
        {"attendances": attendances, "form": form},
    )


@login_required
def one_staff_attendance(request):
    form = StaffIDForm()
    staff = None
    attendance_dict = {}
    total_present_days = 0
    daily_salary = 0
    total_salary_for_present_days = 0
    total_cash_taken = 0
    remaining_salary = 0
    previous_remaining_salary = 0
    combined_remaining_salary = 0
    monthly_salary = 0

    if request.method == "POST":
        form = StaffIDForm(request.POST)
        if form.is_valid():
            staff_id = form.cleaned_data["staff_id"]
            month = form.cleaned_data["month"]

            try:
                staff = Staff.objects.get(staff_id=staff_id)
                month_start = month.replace(day=1)
                monthly_salary = staff.salary
                month_end = month.replace(day=monthrange(month.year, month.month)[1])

                # Calculate previous month's remaining salary
                prev_month_end = month_start - timedelta(days=1)
                prev_month_start = prev_month_end.replace(day=1)

                prev_attendances = Attendance.objects.filter(
                    staff=staff, date__range=(prev_month_start, prev_month_end)
                )
                prev_total_present_days = sum(
                    1 for att in prev_attendances if att.status == "present"
                )
                prev_days_in_month = (prev_month_end - prev_month_start).days + 1
                prev_daily_salary = staff.salary / prev_days_in_month
                prev_total_salary_for_present_days = math.ceil(
                    prev_daily_salary * prev_total_present_days
                )
                prev_total_cash_taken = (
                    Cash.objects.filter(
                        staff=staff, date__range=(prev_month_start, prev_month_end)
                    ).aggregate(total=models.Sum("amount"))["total"]
                    or 0
                )
                previous_remaining_salary = (
                    prev_total_salary_for_present_days - prev_total_cash_taken
                )

                # Calculate current month's attendance and salary
                attendances = Attendance.objects.filter(
                    staff=staff, date__range=(month_start, month_end)
                ).order_by("date")

                all_days = [
                    month_start + timedelta(days=i)
                    for i in range((month_end - month_start).days + 1)
                ]

                for day in all_days:
                    if day < staff.add_date:
                        attendance_dict[day] = "absent"
                        continue

                    attendance = next(
                        (att for att in attendances if att.date == day), None
                    )
                    if attendance:
                        if day.weekday() == FRIDAY:
                            attendance.status = "present"
                            attendance.save()
                        attendance_dict[day] = attendance.status
                    else:
                        if day.weekday() == FRIDAY and day <= datetime.now().date():
                            attendance_dict[day] = "present"
                        else:
                            attendance_dict[day] = "absent"

                total_present_days = sum(
                    1 for status in attendance_dict.values() if status == "present"
                )

                days_in_month = (month_end - month_start).days + 1
                daily_salary = staff.salary / days_in_month
                total_salary_for_present_days = math.ceil(
                    daily_salary * total_present_days
                )

                total_cash_taken = (
                    Cash.objects.filter(
                        staff=staff, date__range=(month_start, month_end)
                    ).aggregate(total=models.Sum("amount"))["total"]
                    or 0
                )

                remaining_salary = total_salary_for_present_days - total_cash_taken

                # Combine previous and current remaining salaries
                combined_remaining_salary = previous_remaining_salary + remaining_salary

            except Staff.DoesNotExist:
                messages.error(request, "Invalid Staff ID. Please try again.")

    return render(
        request,
        "staff/one_staff_attendance.html",
        {
            "form": form,
            "staff": staff,
            "attendance_dict": attendance_dict,
            "total_present_days": total_present_days,
            "total_salary_for_present_days": total_salary_for_present_days,
            "total_cash_taken": total_cash_taken,
            "remaining_salary": remaining_salary,
            "previous_remaining_salary": previous_remaining_salary,
            "combined_remaining_salary": combined_remaining_salary,
            "monthly_salary": monthly_salary,
        },
    )


def add_cash(request):
    if request.method == "POST":
        form = CashForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cash_list")
    else:
        form = CashForm()
    return render(request, "staff/add_cash.html", {"form": form})


def cash_list(request):
    form = CashFilterForm(request.GET or None)
    if form.is_valid():
        day = form.cleaned_data.get("day")
        cash_entries = Cash.objects.filter(date=day).order_by("-date")
    else:
        cash_entries = Cash.objects.filter(date=date.today()).order_by("-date")

    return render(
        request, "staff/cash_list.html", {"cash_entries": cash_entries, "form": form}
    )


@login_required
def one_staff_cash(request):
    form = StaffCashForm()
    staff = None
    cash_records = []
    total_cash_taken = 0

    if request.method == "POST":
        form = StaffCashForm(request.POST)
        if form.is_valid():
            staff_id = form.cleaned_data["staff_id"]
            month = form.cleaned_data["month"]

            try:
                staff = get_object_or_404(Staff, staff_id=staff_id)
                month_start = month.replace(day=1)
                month_end = month.replace(day=monthrange(month.year, month.month)[1])

                cash_records = Cash.objects.filter(
                    staff=staff, date__range=(month_start, month_end)
                ).order_by("date")

                # Calculate total cash taken this month
                total_cash_taken = sum(record.amount for record in cash_records)
            except:
                messages.error(request, "Invalid Staff ID. Please try again.")
    return render(
        request,
        "staff/one_staff_cash.html",
        {
            "form": form,
            "staff": staff,
            "cash_records": cash_records,
            "total_cash_taken": total_cash_taken,
        },
    )


@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return render(request, "staff/home.html")
    else:
        try:
            staff = Staff.objects.get(staff_id=request.user.username)
            attendance = Attendance.objects.filter(staff=staff)
            cash_transactions = Cash.objects.filter(staff=staff)
            context = {
                "staff": staff,
                "attendance": attendance,
                "cash_transactions": cash_transactions,
            }
            return render(request, "staff_desh_area/staff_dashboard.html", context)
        except Staff.DoesNotExist:
            return render(
                request, "staff/error.html", {"message": "Staff record not found."}
            )


# admin are start here sir
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_dashboard")
            else:
                messages.error(request, "Invalid login Username/Password ")  # Error message
    else:
        form = LoginForm()

    return render(request, "staff/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
