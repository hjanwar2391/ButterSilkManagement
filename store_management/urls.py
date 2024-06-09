from django.urls import path
from . import views

urlpatterns = [
    path("add_store/", views.add_store, name="add_store"),
    path("store_list/", views.store_list, name="store_list"),
    path("add_product/", views.add_product, name="add_product"),
    path("add_daily_sales/", views.add_daily_sales, name="add_daily_sales"),
    path("add_deposit_amount/", views.add_deposit_amount, name="add_deposit_amount"),
    path("deposit_amount_list/", views.deposit_amount_list, name="deposit_amount_list"),
    path("list_daily_sales/", views.list_daily_sales, name="list_daily_sales"),
    path("product-list/", views.product_list, name="product_list"),
]
