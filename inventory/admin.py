from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ["name", "sku", "price", "stock_quantity"]
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description_preview", "product_count", "created_at"]
    search_fields = ["name", "description"]
    inlines = [ProductInline]

    @admin.display(description="Description")
    def description_preview(self, obj):
        if not obj.description:
            return "-"
        return obj.description[:60] + ("..." if len(obj.description) > 60 else "")

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sku",
        "category",
        "price",
        "stock_quantity",
        "stock_status_badge",
        "created_at",
    ]
    list_filter = ["category", "created_at"]
    search_fields = ["name", "sku", "description"]
    list_editable = ["stock_quantity"]
    list_per_page = 25
    autocomplete_fields = ["category"]

    @admin.display(description="Stock Status")
    def stock_status_badge(self, obj):
        if obj.stock_quantity <= 5:
            color = "#dc3545"  # red
            text = f"Low ({obj.stock_quantity})"
        elif obj.stock_quantity <= 20:
            color = "#ffc107"  # yellow/amber
            text = f"Medium ({obj.stock_quantity})"
        else:
            color = "#198754"  # green
            text = f"Healthy ({obj.stock_quantity})"
        text_color = "#000" if obj.stock_quantity > 5 and obj.stock_quantity <= 20 else "#fff"
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">{}</span>',
            color,
            text_color,
            text,
        )
