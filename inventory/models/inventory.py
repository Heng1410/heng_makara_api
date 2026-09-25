from django.db import models


from base.models.base_model import BaseModel
from plants.models.plants import Plant


class Inventory(BaseModel):
    plant = models.OneToOneField(
        Plant, on_delete=models.PROTECT, related_name="inventory"
    )

    quantity = models.PositiveIntegerField(default=0)

    low_stock_threshold = models.PositiveIntegerField(default=5)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "inventory"
        ordering = ["-created_at"]
