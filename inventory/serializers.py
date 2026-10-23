from decimal import Decimal
from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "product_count",
            "created_at",
        ]

    def validate_name(self, value):
        trimmed = value.strip()
        if not trimmed:
            raise serializers.ValidationError("Category name cannot be empty.")
        # Check uniqueness case-insensitively, excluding current instance if updating
        queryset = Category.objects.filter(name__iexact=trimmed)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(f"Category with name '{trimmed}' already exists.")
        return trimmed


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    stock_status = serializers.CharField(read_only=True)
    stock_status_label = serializers.CharField(read_only=True)
    total_value = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "sku",
            "category",
            "category_name",
            "stock_quantity",
            "stock_status",
            "stock_status_label",
            "total_value",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value):
        if value < Decimal("0.01"):
            raise serializers.ValidationError("Price must be at least 0.01.")
        return value

    def validate_sku(self, value):
        trimmed = value.strip()
        if not trimmed:
            raise serializers.ValidationError("SKU cannot be blank.")
        queryset = Product.objects.filter(sku__iexact=trimmed)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(f"Product with SKU '{trimmed}' already exists.")
        return trimmed.upper()

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
