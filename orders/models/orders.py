from django.conf import settings
from django.db import models

from base.models.base_model import BaseModel
from orders.constants import (
    ORDER_STATUSES,
    ORDER_STATUS_PENDING,
)


class Order(BaseModel):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUSES,
        default=ORDER_STATUS_PENDING,
    )

    class Meta:
        ordering = ["-created_at"]