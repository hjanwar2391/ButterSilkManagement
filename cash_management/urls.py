from django.urls import path
from . import views

urlpatterns = [
    path("cash_add_cash/", views.add_cash, name="cash_add_cash"),
    path("cash_cash_list/", views.cash_list, name="cash_cash_list"),
    path("add_spend_cash/", views.spend_cash, name="add_spent_cash"),
    path("cash_spent_list/", views.cash_spent_list, name="cash_spent_list"),
    path("current_balance/", views.current_balance, name="current_balance"),
    path('cash_overview/', views.cash_overview, name='cash_overview'),  # New URL pattern
    path('monthly_cash_overview/', views.monthly_Cash_Overview, name='monthly_cash_overview'),  # monthly cash overview show here
]
