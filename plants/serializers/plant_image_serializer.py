from rest_framework import serializers

from plants.models.plant_images import PlantImage


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = [
            "id",
            "image",
            "image_type",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]