from django.db import transaction

from inventory.constants import StockMovementType
from inventory.models.inventory import Inventory
from inventory.services.inventory_service import InventoryService


class OrderInventoryService:

    @staticmethod
    @transaction.atomic
    def deduct_for_order(order):
        for item in order.items.select_related("plant").all():
            inventory = Inventory.objects.get(plant=item.plant)

            InventoryService.remove_stock(
                inventory_id=inventory.id,
                quantity=item.quantity,
                movement_type=StockMovementType.SALE,
                reference_type="ORDER",
                reference_id=str(order.id),
                reason=f"Stock deducted for order #{order.id}",
            )
