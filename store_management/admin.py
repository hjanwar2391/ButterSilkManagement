from django.contrib import admin
from .models import Store, Product, DailySales, DepositAmount


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("store_id", "name", "address")
    search_fields = ("name", "store_id")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "store", "quantity", "invoice_no", "date_added")
    search_fields = ("name", "invoice_no")
    list_filter = ("store", "date_added")


@admin.register(DailySales)
class DailySalesAdmin(admin.ModelAdmin):
    list_display = (
        "store",
        "product",
        "date",
        "sell_amount",
        "sell_due",
        "sell_quantity_products",
        "return_product_quantity",
        "cost_amount",
    )
    search_fields = ("store__name", "product__name", "date")
    list_filter = ("store", "date")


@admin.register(DepositAmount)
class DepositAmountAdmin(admin.ModelAdmin):
    list_display = ("store", "date", "amount")
    search_fields = ("store__name", "date")
    list_filter = ("store", "date")
