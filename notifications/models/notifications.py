from django.conf import settings
from django.db import models

from base.models.base_model import BaseModel


class Notification(BaseModel):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=255,
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
    )

    is_read = models.BooleanField(
        default=False,
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )