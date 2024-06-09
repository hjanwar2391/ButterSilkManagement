from django.db import models


class CashAdd(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type =  models.CharField(max_length=10, default='Added')

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"


class CashSpent(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, default='Spent')
    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
