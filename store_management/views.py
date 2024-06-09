from django.shortcuts import render, get_object_or_404, redirect
from .models import Store, Product, DailySales, DepositAmount
from .forms import (
    StoreForm,
    ProductForm,
    DailySalesForm,
    DepositAmountForm,
    DateFilterForm,
    StoreIDForm
)
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from .forms import DateFilterForm
from datetime import datetime, timedelta
from django.db.models import Sum
from calendar import monthrange
from .models import Store, DailySales, DepositAmount
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Store, DailySales
from .forms import StoreMonthForm


def add_store(request):
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Store added successfully!")
            form = StoreForm()
        else:
            # If form is not valid, display error message
            messages.error(
                request, "Failed to add store. Please correct the errors below."
            )
    else:
        form = StoreForm()
    return render(request, "store/add_store.html", {"form": form})


# store list show logic
def store_list(request):
    number_of_store = Store.objects.all()
    return render(
        request, "store/store_list.html", {"number_of_store": number_of_store}
    )


#  add product logic here
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            form = ProductForm()

        else:
            # If form is not valid, display error message
            messages.error(
                request, "Failed to add product. Please correct the errors below."
            )
    else:
        form = ProductForm()
    return render(request, "store/add_product.html", {"form": form})


def add_daily_sales(request):
    if request.method == "POST":
        form = DailySalesForm(request.POST)
        if form.is_valid():
            daily_sales = form.save(commit=False)
            if daily_sales.product:
                daily_sales.save()
                messages.success(request, "Sales added successfully!")
                form = DailySalesForm()
            else:
                messages.error(request, "Product must be selected.")
        else:
            messages.error(
                request, "Failed to add sales. Please correct the errors below."
            )
    else:
        form = DailySalesForm()
    return render(request, "store/add_daily_sales.html", {"form": form})


def product_list(request):
    products = Product.objects.all().select_related("store")
    store_totals = Product.objects.values(
        "store__id", "store__name", "store__store_id"
    ).annotate(total_quantity=Sum("quantity"))

    context = {
        "products": products,
        "store_totals": store_totals,
    }

    return render(request, "store/product_list.html", context)


def add_deposit_amount(request):
    if request.method == "POST":
        form = DepositAmountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Deposit added successfully!")
            form = DepositAmountForm()
        else:
            messages.error(
                request, "Failed to add Deposit. Please correct the errors below."
            )

    else:
        form = DepositAmountForm()
    return render(request, "store/add_deposit_amount.html", {"form": form})


def deposit_amount_list(request):
    form = StoreIDForm(request.POST or None)
    deposit_amounts = None
    total_deposit = 0

    if request.method == "POST":
        if form.is_valid():
            store_id = form.cleaned_data["store_id"]
            current_month = datetime.now().month
            current_year = datetime.now().year
            deposit_amounts = DepositAmount.objects.filter(
                store__store_id=store_id,
                date__year=current_year,
                date__month=current_month,
            ).order_by("date")

            total_deposit = sum(
                deposit_amount.amount for deposit_amount in deposit_amounts
            )

    context = {
        "form": form,
        "deposit_amounts": deposit_amounts,
        "total_deposit": total_deposit,
    }

    return render(request, "store/deposit_amount_list.html", context)


def list_daily_sales(request):
    form = DateFilterForm(request.GET or None)
    today = timezone.now().date()

    # Set default filter to today if no dates are provided
    if request.GET.get("start_date") or request.GET.get("end_date"):
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            if start_date and end_date:
                sales = DailySales.objects.filter(date__range=[start_date, end_date])
            elif start_date:
                sales = DailySales.objects.filter(date__gte=start_date)
            elif end_date:
                sales = DailySales.objects.filter(date__lte=end_date)
    else:
        sales = DailySales.objects.filter(date=today)

    # Calculate totals
    total_cost_amount = sales.aggregate(Sum("cost_amount"))["cost_amount__sum"] or 0
    total_sell_quantity = (
        sales.aggregate(Sum("sell_quantity_products"))["sell_quantity_products__sum"]
        or 0
    )
    total_sell_amount = sales.aggregate(Sum("sell_amount"))["sell_amount__sum"] or 0

    return render(
        request,
        "store/list_daily_sales.html",
        {
            "form": form,
            "sales": sales,
            "total_cost_amount": total_cost_amount,
            "total_sell_quantity": total_sell_quantity,
            "total_sell_amount": total_sell_amount,
        },
    )
