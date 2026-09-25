from django.urls import path

from inventory.views.inventory_adjustment_view import InventoryAdjustmentView
from inventory.views.inventory_restock_view import InventoryRestockView
from inventory.views.inventory_restock_view import InventoryRestockView
from inventory.views.inventory_view import (
    InventoryDetailView,
    InventoryListView,
)
from inventory.views.stock_movement_view import (
    StockMovementDetailView,
    StockMovementListView,
)

urlpatterns = [
    path(
        "",
        InventoryListView.as_view(),
        name="inventory-list",
    ),
    path(
        "movements/",
        StockMovementListView.as_view(),
        name="stock-movement-list",
    ),
    path(
        "movements/<int:pk>/",
        StockMovementDetailView.as_view(),
        name="stock-movement-detail",
    ),
    path(
        "<int:pk>/",
        InventoryDetailView.as_view(),
        name="inventory-detail",
    ),
    path(
        "<int:pk>/restock/",
        InventoryRestockView.as_view(),
        name="inventory-restock",
    ),
    path(
        "<int:pk>/adjust/",
        InventoryAdjustmentView.as_view(),
        name="inventory-adjust",
    ),
]
