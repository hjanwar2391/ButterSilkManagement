from django.shortcuts import render, redirect
from .models import CashAdd, CashSpent
from .forms import CashAddForm, CashSpentForm, MonthlyCashOverViewForm, CashFilterForm
from django.utils.timezone import now
from django.contrib import messages
from itertools import chain
from operator import attrgetter
from calendar import monthrange
from datetime import datetime


def add_cash(request):
    if request.method == "POST":
        form = CashAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cash added successfully!")
            return redirect("cash_add_cash")
        else:
            # If form is not valid, display error message
            messages.error(
                request, "Failed to add cash. Please correct the errors below."
            )
    else:
        form = CashAddForm()
    return render(request, "cash/add_cash.html", {"form": form})


def cash_list(request):
    today = now().date()
    cash_adds = CashAdd.objects.filter(date=today)
    total_cash = sum(cash.amount for cash in cash_adds)
    return render(
        request,
        "cash/cash_list.html",
        {
            "cash_adds": cash_adds,
            "total_cash": total_cash,
        },
    )


def spend_cash(request):
    if request.method == "POST":
        form = CashSpentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cash_spent_list")
    else:
        form = CashSpentForm()
    return render(request, "cash/spend_cash.html", {"form": form})


def cash_spent_list(request):
    today = now().date()
    cash_spents = CashSpent.objects.filter(date=today)
    total_spent = sum(cash.amount for cash in cash_spents)
    return render(
        request,
        "cash/cash_spent_list.html",
        {
            "cash_spents": cash_spents,
            "total_spent": total_spent,
        },
    )


def current_balance(request):
    total_cash = sum(cash.amount for cash in CashAdd.objects.all())
    total_spent = sum(cash.amount for cash in CashSpent.objects.all())
    current_balance = total_cash - total_spent
    return render(
        request,
        "cash_management/current_balance.html",
        {
            "current_balance": current_balance,
        },
    )


def cash_overview(request):
    form = CashFilterForm(request.GET or None)
    selected_date = (
        form.cleaned_data["day"] if form.is_valid() else datetime.now().date()
    )

    cash_adds = CashAdd.objects.filter(date=selected_date)
    cash_spents = CashSpent.objects.filter(date=selected_date)

    # Combine and sort the entries by date
    combined_list = sorted(chain(cash_adds, cash_spents), key=attrgetter("date"))

    # Calculate totals
    total_added = sum(cash.amount for cash in cash_adds)
    total_spent = sum(cash.amount for cash in cash_spents)
    current_balance = total_added - total_spent

    return render(
        request,
        "cash/cash_overview.html",
        {
            "form": form,
            "combined_list": combined_list,
            "total_added": total_added,
            "total_spent": total_spent,
            "current_balance": current_balance,
        },
    )


def monthly_Cash_Overview(request):
    # Get the current month and year
    current_date = datetime.now()
    initial_data = current_date.strftime("%Y-%m")

    form = MonthlyCashOverViewForm(
        request.POST or None, initial={"month": initial_data}
    )

    if request.method == "POST" and form.is_valid():
        month_year = form.cleaned_data["month"]
        month = month_year.month
        year = month_year.year

        # Filter cash adds and cash spents for the selected month and year
        month_start = datetime(year, month, 1).date()
        month_end = month_start.replace(day=monthrange(year, month)[1])

        cash_adds = CashAdd.objects.filter(date__range=[month_start, month_end])
        cash_spents = CashSpent.objects.filter(date__range=[month_start, month_end])

        # Combine and sort the entries by date
        combined_list = sorted(chain(cash_adds, cash_spents), key=attrgetter("date"))

        # Calculate totals
        total_added = sum(cash.amount for cash in cash_adds)
        total_spent = sum(cash.amount for cash in cash_spents)
        current_balance = total_added - total_spent

        return render(
            request,
            "cash/monthly_cash_overview.html",
            {
                "form": form,
                "combined_list": combined_list,
                "total_added": total_added,
                "total_spent": total_spent,
                "current_balance": current_balance,
            },
        )

    return render(
        request,
        "cash/monthly_cash_overview.html",
        {
            "form": form,
        },
    )
