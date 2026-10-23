import json
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db.models import F, Sum, Count, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CategoryForm, ProductForm
from .models import Category, Product


def dashboard_view(request):
    """
    Dashboard (/)
    4 stat cards + bar chart + pie chart + low-stock table (qty <= 5)
    """
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    low_stock_products = (
        Product.objects.filter(stock_quantity__lte=5)
        .select_related("category")
        .order_by("stock_quantity")
    )
    low_stock_count = low_stock_products.count()

    total_stock_value = Product.objects.aggregate(
        total=Sum(
            F("price") * F("stock_quantity"),
            output_field=models.DecimalField(max_digits=14, decimal_places=2),
        )
    )["total"] or Decimal("0.00")

    # Category aggregations for charts
    cat_stats = (
        Category.objects.annotate(
            stock_value=Coalesce(
                Sum(
                    F("products__price") * F("products__stock_quantity"),
                    output_field=models.DecimalField(max_digits=14, decimal_places=2),
                ),
                Decimal("0.00"),
                output_field=models.DecimalField(max_digits=14, decimal_places=2),
            ),
            product_count=Count("products"),
        )
        .order_by("name")
    )

    chart_categories = [c.name for c in cat_stats]
    chart_stock_values = [float(c.stock_value) for c in cat_stats]
    chart_product_counts = [c.product_count for c in cat_stats]

    context = {
        "active_tab": "dashboard",
        "total_products": total_products,
        "total_categories": total_categories,
        "low_stock_count": low_stock_count,
        "total_stock_value": total_stock_value,
        "low_stock_products": low_stock_products[:10],
        "chart_categories_json": json.dumps(chart_categories),
        "chart_stock_values_json": json.dumps(chart_stock_values),
        "chart_product_counts_json": json.dumps(chart_product_counts),
    }
    return render(request, "inventory/dashboard.html", context)


def product_list_view(request):
    """
    Product List (/products/)
    Search, filters, sort, pagination, and stock status badges
    """
    queryset = Product.objects.select_related("category").all()
    categories = Category.objects.all().order_by("name")

    search_query = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    in_stock = request.GET.get("in_stock", "").strip()
    ordering = request.GET.get("ordering", "-created_at").strip()

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(sku__icontains=search_query)
        )

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    if min_price:
        try:
            queryset = queryset.filter(price__gte=Decimal(min_price))
        except (InvalidOperation, ValueError):
            pass

    if max_price:
        try:
            queryset = queryset.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            pass

    if in_stock in ("true", "1", "on"):
        queryset = queryset.filter(stock_quantity__gt=0)

    allowed_orderings = {
        "name": "name",
        "-name": "-name",
        "price": "price",
        "-price": "-price",
        "stock_quantity": "stock_quantity",
        "-stock_quantity": "-stock_quantity",
        "created_at": "created_at",
        "-created_at": "-created_at",
    }
    sort_key = allowed_orderings.get(ordering, "-created_at")
    queryset = queryset.order_by(sort_key)

    # Build querystring preserving filters (excluding page)
    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    preserved_query = query_params.urlencode()

    total_filtered_count = queryset.count()
    paginator = Paginator(queryset, 10)  # 10 products per page
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "active_tab": "products",
        "page_obj": page_obj,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "in_stock": in_stock in ("true", "1", "on"),
        "ordering": ordering,
        "total_filtered_count": total_filtered_count,
        "preserved_query": preserved_query,
    }
    return render(request, "inventory/product_list.html", context)


def product_create_view(request):
    """
    Product Create (/products/new/)
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was created successfully.")
            return redirect("inventory:product_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductForm()

    context = {
        "active_tab": "products",
        "form": form,
        "title": "Add New Product",
        "is_create": True,
    }
    return render(request, "inventory/product_form.html", context)


def product_update_view(request, pk):
    """
    Product Edit (/products/<id>/edit/)
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was updated successfully.")
            return redirect("inventory:product_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductForm(instance=product)

    context = {
        "active_tab": "products",
        "form": form,
        "product": product,
        "title": f"Edit Product: {product.name}",
        "is_create": False,
    }
    return render(request, "inventory/product_form.html", context)


def product_delete_view(request, pk):
    """
    Product Delete confirmation & POST action (/products/<id>/delete/)
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' has been deleted.")
        return redirect("inventory:product_list")

    return render(
        request,
        "inventory/product_confirm_delete.html",
        {"product": product, "active_tab": "products"},
    )


def category_list_view(request):
    """
    Category CRUD (/categories/)
    List with product counts, add new category inline/form
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' was created successfully.")
            return redirect("inventory:category_list")
        else:
            messages.error(request, "Could not create category. Please check form errors.")
    else:
        form = CategoryForm()

    categories = (
        Category.objects.annotate(
            product_count=Count("products"),
            total_stock_value=Coalesce(
                Sum(
                    F("products__price") * F("products__stock_quantity"),
                    output_field=models.DecimalField(max_digits=14, decimal_places=2),
                ),
                Decimal("0.00"),
                output_field=models.DecimalField(max_digits=14, decimal_places=2),
            ),
        )
        .order_by("name")
    )

    context = {
        "active_tab": "categories",
        "categories": categories,
        "form": form,
    }
    return render(request, "inventory/category_list.html", context)


def category_update_view(request, pk):
    """
    Category Edit (/categories/<id>/edit/)
    """
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' updated successfully.")
            return redirect("inventory:category_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "inventory/category_form.html",
        {
            "form": form,
            "category": category,
            "title": f"Edit Category: {category.name}",
            "active_tab": "categories",
        },
    )


def category_delete_view(request, pk):
    """
    Category Delete (/categories/<id>/delete/)
    Blocks deletion when products exist, shows friendly error message
    """
    category = get_object_or_404(Category, pk=pk)
    product_count = category.products.count()

    if request.method == "POST":
        if product_count > 0:
            messages.error(
                request,
                f"Cannot delete category '{category.name}' because it contains {product_count} active product(s). Please reassign or delete these products first.",
            )
            return redirect("inventory:category_list")

        try:
            name = category.name
            category.delete()
            messages.success(request, f"Category '{name}' was deleted.")
            return redirect("inventory:category_list")
        except models.ProtectedError:
            messages.error(
                request,
                f"Cannot delete category '{category.name}' because it is protected by associated products.",
            )
            return redirect("inventory:category_list")

    return render(
        request,
        "inventory/category_confirm_delete.html",
        {
            "category": category,
            "product_count": product_count,
            "active_tab": "categories",
        },
    )
