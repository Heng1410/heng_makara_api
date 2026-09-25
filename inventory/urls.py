from django.urls import path

from inventory.views.inventory_restock_view import InventoryRestockView
from inventory.views.inventory_restock_view import InventoryRestockView
from inventory.views.inventory_view import (
    InventoryDetailView,
    InventoryListView,
)

urlpatterns = [
    path(
        "",
        InventoryListView.as_view(),
        name="inventory-list",
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
]
