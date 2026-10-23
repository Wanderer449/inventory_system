from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def stock_status(self):
        if self.stock_quantity <= 5:
            return "danger"
        elif self.stock_quantity <= 20:
            return "warning"
        return "success"

    @property
    def stock_status_label(self):
        if self.stock_quantity <= 5:
            return "Low Stock"
        elif self.stock_quantity <= 20:
            return "Medium"
        return "In Stock"

    @property
    def total_value(self):
        return self.price * self.stock_quantity
