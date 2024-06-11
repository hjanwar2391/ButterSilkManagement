from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add_staff/", views.add_staff, name="add_staff"),
    path("staff_list/", views.staff_list, name="staff_list"),
    path("add_attendance/", views.add_attendance, name="add_attendance"),
    path("attendance_list/", views.attendance_list, name="attendance_list"),
    path(
        "one_staff_attendance/",
        views.one_staff_attendance,
        name="one_staff_attendance",
    ),
    path("add_cash/", views.add_cash, name="add_cash"),
    path("cash_list/", views.cash_list, name="cash_list"),
    path("one_staff_cash/", views.one_staff_cash, name="one_staff_cash"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
  
    
]
