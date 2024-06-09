from django.db import models
from django.db.models import F


class Store(models.Model):
    name = models.CharField(max_length=100)
    store_id = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    invoice_no = models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class DailySales(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateField(auto_now_add=True)
    sell_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sell_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sell_quantity_products = models.PositiveIntegerField()
    return_product_quantity = models.PositiveIntegerField(default=0)
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True, default="Note If Needed")

    def __str__(self):
        return f"Sales on {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.product:
            # Update product quantity
            Product.objects.filter(pk=self.product.pk).update(
                quantity=F("quantity")
                - self.sell_quantity_products
                + self.return_product_quantity
            )


class DepositAmount(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Deposit on {self.date}"
