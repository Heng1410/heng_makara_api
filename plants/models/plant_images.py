from django.db import models

from base.models.base_model import BaseModel
from plants.constants import (
    PLANT_IMAGE_TYPES,
    PLANT_IMAGE_TYPE_MAIN,
    PLANT_IMAGE_TYPE_SUB,
)
from plants.models.plants import Plant


class PlantImage(BaseModel):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="plants/",
    )

    image_type = models.CharField(
        max_length=10,
        choices=PLANT_IMAGE_TYPES,
        default=PLANT_IMAGE_TYPE_SUB,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["plant"],
                condition=models.Q(
                    image_type=PLANT_IMAGE_TYPE_MAIN,
                ),
                name="unique_main_image_per_plant",
            ),
        ]