from rest_framework import serializers

from plants.models.plants import Plant
from plants.serializers.plant_image_serializer import PlantImageSerializer


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            "name",
            "scientific_name",
            "description",
            "category",
            "estimated_price",
            "stock_quantity",
            "is_available",
            "is_featured",
        ]


class PlantListSerializer(PlantSerializer):
    class Meta(PlantSerializer.Meta):
        fields = [
            "id",
            "name",
            "category",
            "estimated_price",
            "is_available",
            "is_featured",
        ]


class PlantDetailSerializer(PlantSerializer):
    images = PlantImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta(PlantSerializer.Meta):
        fields = [
            "id",
            "name",
            "scientific_name",
            "description",
            "category",
            "estimated_price",
            "stock_quantity",
            "is_available",
            "is_featured",
            "images",
            "created_at",
            "updated_at",
        ]