from rest_framework import serializers

from inventory.models.stock_movement import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            "id",
            "inventory",
            "quantity_before",
            "quantity",
            "quantity_after",
            "movement_type",
            "reference_type",
            "reference_id",
            "reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class StockMovementListSerializer(StockMovementSerializer):
    inventory_plant_name = serializers.CharField(
        source="inventory.plant.name",
        read_only=True,
    )

    class Meta(StockMovementSerializer.Meta):
        fields = [
            "id",
            "inventory",
            "inventory_plant_name",
            "quantity",
            "movement_type",
            "reference_type",
            "reference_id",
            "created_at",
        ]


class StockMovementDetailSerializer(StockMovementSerializer):
    inventory_plant_name = serializers.CharField(
        source="inventory.plant.name",
        read_only=True,
    )

    class Meta(StockMovementSerializer.Meta):
        fields = [
            "id",
            "inventory",
            "inventory_plant_name",
            "quantity_before",
            "quantity",
            "quantity_after",
            "movement_type",
            "reference_type",
            "reference_id",
            "reason",
            "created_at",
            "updated_at",
        ]
