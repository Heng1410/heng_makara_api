from django.db import models

from base.models.base_model import BaseModel
from inventory.constants import StockMovementType
from inventory.models.inventory import Inventory


class StockMovement(BaseModel):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.PROTECT, related_name="movements"
    )

    quantity_before = models.PositiveIntegerField()

    quantity = models.IntegerField()

    quantity_after = models.PositiveIntegerField()

    movement_type = models.CharField(max_length=20, choices=StockMovementType.CHOICES)

    reference_type = models.CharField(max_length=50, blank=True)

    reference_id = models.CharField(max_length=100, blank=True)

    reason = models.TextField(blank=True)

    class Meta:
        db_table = "stock_movement"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["inventory", "-created_at"]),
            models.Index(fields=["movement_type", "-created_at"]),
        ]
