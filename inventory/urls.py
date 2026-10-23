from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_api, views_ui

app_name = "inventory"

router = DefaultRouter()
router.register(r"categories", views_api.CategoryViewSet, basename="category-api")
router.register(r"products", views_api.ProductViewSet, basename="product-api")

urlpatterns = [
    # Server-rendered Frontend URLs
    path("", views_ui.dashboard_view, name="dashboard"),
    path("products/", views_ui.product_list_view, name="product_list"),
    path("products/new/", views_ui.product_create_view, name="product_create"),
    path("products/<int:pk>/edit/", views_ui.product_update_view, name="product_edit"),
    path("products/<int:pk>/delete/", views_ui.product_delete_view, name="product_delete"),
    path("categories/", views_ui.category_list_view, name="category_list"),
    path("categories/<int:pk>/edit/", views_ui.category_update_view, name="category_edit"),
    path("categories/<int:pk>/delete/", views_ui.category_delete_view, name="category_delete"),
    # REST API endpoints
    path("api/dashboard/summary/", views_api.dashboard_summary_api, name="api_dashboard_summary"),
    path("api/dashboard/chart/", views_api.dashboard_chart_api, name="api_dashboard_chart"),
    path("api/", include(router.urls)),
]
