import django_filters

from inventory.models.stock_movement import StockMovement


class StockMovementFilter(django_filters.FilterSet):

    inventory = django_filters.NumberFilter(
        field_name="inventory_id",
    )

    movement_type = django_filters.CharFilter(
        field_name="movement_type",
    )

    class Meta:
        model = StockMovement
        fields = [
            "inventory",
            "movement_type",
        ]