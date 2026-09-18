from django.db import models

from base.models.base_model import BaseModel
from plants.constants import (
    PLANT_CATEGORIES,
    PLANT_CATEGORY_OTHER,
)


class Plant(BaseModel):
    name = models.CharField(
        max_length=255,
    )

    scientific_name = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    category = models.CharField(
        max_length=50,
        choices=PLANT_CATEGORIES,
        default=PLANT_CATEGORY_OTHER,
    )

    estimated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
    )

    is_available = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-created_at"]