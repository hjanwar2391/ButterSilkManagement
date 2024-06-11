from django.contrib import admin
from .models import Staff, Attendance, Cash


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "name", "phone", "salary", "add_date")
    search_fields = ("name", "staff_id")
    list_filter = ("add_date",)
    ordering = ("staff_id",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("staff", "date", "status")
    search_fields = ("staff__name",)
    list_filter = ("date", "status")
    ordering = ("date",)


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ("staff", "amount", "description", "date")
    search_fields = ("staff__name", "description")
    list_filter = ("date",)
    ordering = ("date",)


# Alternatively, you can use the simpler method if no customization is needed:
# admin.site.register(Staff)
# admin.site.register(Attendance)
# admin.site.register(Cash)
