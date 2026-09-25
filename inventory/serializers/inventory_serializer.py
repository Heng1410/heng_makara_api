from rest_framework import serializers

from inventory.models.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            "id",
            "plant",
            "quantity",
            "low_stock_threshold",
            "is_low_stock",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "quantity",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]

    def get_is_low_stock(self, obj):
        return obj.quantity <= obj.low_stock_threshold


class InventoryListSerializer(InventorySerializer):
    plant_name = serializers.CharField(
        source="plant.name",
        read_only=True,
    )

    class Meta(InventorySerializer.Meta):
        fields = [
            "id",
            "plant",
            "plant_name",
            "quantity",
            "low_stock_threshold",
            "is_low_stock",
            "is_active",
        ]


class InventoryDetailSerializer(InventorySerializer):
    plant_name = serializers.CharField(
        source="plant.name",
        read_only=True,
    )

    class Meta(InventorySerializer.Meta):
        fields = [
            "id",
            "plant",
            "plant_name",
            "quantity",
            "low_stock_threshold",
            "is_low_stock",
            "is_active",
            "created_at",
            "updated_at",
        ]