from decimal import Decimal
from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Electronics, Office Supplies",
                    "id": "id_category_name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief description of the category (optional)",
                    "id": "id_category_description",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Category name cannot be empty.")
        qs = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"A category named '{name}' already exists.")
        return name


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "category",
            "price",
            "stock_quantity",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product title or brand & model",
                    "id": "id_product_name",
                }
            ),
            "sku": forms.TextInput(
                attrs={
                    "class": "form-control text-uppercase",
                    "placeholder": "e.g., ELEC-1001",
                    "id": "id_product_sku",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_product_category",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "0.00",
                    "id": "id_product_price",
                }
            ),
            "stock_quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "placeholder": "0",
                    "id": "id_product_stock_quantity",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional detailed specifications or notes",
                    "id": "id_product_description",
                }
            ),
        }

    def clean_sku(self):
        sku = self.cleaned_data.get("sku", "").strip().upper()
        if not sku:
            raise forms.ValidationError("SKU cannot be blank.")
        qs = Product.objects.filter(sku__iexact=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f"Product with SKU '{sku}' already exists.")
        return sku

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < Decimal("0.01"):
            raise forms.ValidationError("Price must be at least ₹0.01.")
        return price

    def clean_stock_quantity(self):
        stock = self.cleaned_data.get("stock_quantity")
        if stock is not None and stock < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock
