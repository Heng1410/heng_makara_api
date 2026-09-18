from rest_framework import serializers

from orders.models.order_item import OrderItem
from orders.models.orders import Order
from plants.models.plants import Plant
from plants.serializers.plants_serializer import PlantListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    plant = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(),
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "plant",
            "quantity",
            "unit_price",
        ]
        read_only_fields = [
            "id",
            "unit_price",
        ]


class OrderItemListSerializer(serializers.ModelSerializer):
    plant = PlantListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "plant",
            "quantity",
            "unit_price",
        ]
        read_only_fields = [
            "id",
            "unit_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_items(self, items):
        plant_ids = [item["plant"].id for item in items]

        if len(plant_ids) != len(set(plant_ids)):
            raise serializers.ValidationError(
                "A plant can only appear once in an order."
            )
            
        return items


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(read_only=True, many=True)
    total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )


    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total",
            "items",
            "created_at",
            "updated_at",
        ]
