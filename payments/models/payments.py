from django.db import models

from base.models.base_model import BaseModel
from orders.models.orders import Order
from payments.constants import PAYMENT_METHODS, PAYMENT_STATUS_PENDING, PAYMENT_STATUSES


class Payment(BaseModel):
    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="payment",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUSES,
        default=PAYMENT_STATUS_PENDING,
    )

    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )