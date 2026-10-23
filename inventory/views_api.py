from decimal import Decimal, InvalidOperation
from django.db import models
from django.db.models import F, Sum, Count, Q
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("products")).order_by("name")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.products.exists():
            return Response(
                {
                    "error": f"Cannot delete category '{instance.name}' because it contains {instance.products.count()} products. Please reassign or delete them first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            return super().destroy(request, *args, **kwargs)
        except models.ProtectedError:
            return Response(
                {"error": "Cannot delete this category because it is protected by associated products."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()
        params = self.request.query_params

        # ?search= (name, description, SKU - icontains)
        search = params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(sku__icontains=search)
            )

        # ?category=<id>
        category_id = params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # ?min_price=
        min_price = params.get("min_price")
        if min_price:
            try:
                queryset = queryset.filter(price__gte=Decimal(min_price))
            except (InvalidOperation, ValueError):
                pass

        # ?max_price=
        max_price = params.get("max_price")
        if max_price:
            try:
                queryset = queryset.filter(price__lte=Decimal(max_price))
            except (InvalidOperation, ValueError):
                pass

        # ?in_stock=true
        in_stock = params.get("in_stock")
        if in_stock and in_stock.lower() in ("true", "1", "yes"):
            queryset = queryset.filter(stock_quantity__gt=0)

        # ?ordering=name|price|stock_quantity (prefix - for desc)
        ordering = params.get("ordering")
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
        if ordering in allowed_orderings:
            queryset = queryset.order_by(allowed_orderings[ordering])

        return queryset


@api_view(["GET"])
def dashboard_summary_api(request):
    """
    GET /api/dashboard/summary/
    Returns total_products, total_stock_value, low_stock_count (qty <= 5), total_categories
    """
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__lte=5).count()

    stock_val = Product.objects.aggregate(
        total_value=Sum(
            F("price") * F("stock_quantity"),
            output_field=models.DecimalField(max_digits=14, decimal_places=2),
        )
    )["total_value"] or Decimal("0.00")

    return Response(
        {
            "total_products": total_products,
            "total_stock_value": float(stock_val),
            "low_stock_count": low_stock_count,
            "total_categories": total_categories,
        }
    )


@api_view(["GET"])
def dashboard_chart_api(request):
    """
    GET /api/dashboard/chart/
    Returns [{ category, stock_value, product_count }] aggregated with Sum(F('price') * F('stock_quantity'))
    """
    categories = Category.objects.annotate(
        stock_value=Coalesce(
            Sum(
                F("products__price") * F("products__stock_quantity"),
                output_field=models.DecimalField(max_digits=14, decimal_places=2),
            ),
            Decimal("0.00"),
            output_field=models.DecimalField(max_digits=14, decimal_places=2),
        ),
        product_count=Count("products"),
    ).order_by("name")

    data = [
        {
            "category": cat.name,
            "stock_value": float(cat.stock_value),
            "product_count": cat.product_count,
        }
        for cat in categories
    ]
    return Response(data)
