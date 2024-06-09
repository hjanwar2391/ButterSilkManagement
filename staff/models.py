from django.db import models
from django.utils import timezone


class Staff(models.Model):
    staff_id = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    add_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = (("present", "Present"), ("absent", "Absent"))
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.staff.name} - {self.status}"


class Cash(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.name if self.staff else 'General'} - {self.amount}"
