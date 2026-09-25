from base.exceptions.base_exception import BadRequestException

from django.db import transaction

from inventory.constants import StockMovementType
from inventory.models.inventory import Inventory
from inventory.models.stock_movement import StockMovement
from inventory.services.low_stock_service import LowStockService


class InventoryService:

    @staticmethod
    @transaction.atomic
    def restock(inventory_id, quantity, reason="", reference_type="", reference_id=""):
        inventory = Inventory.objects.select_for_update().get(id=inventory_id)

        if quantity <= 0:
            raise BadRequestException("Restock quantity must be greater than zero.")

        quantity_before = inventory.quantity
        quantity_after = quantity_before + quantity

        inventory.quantity = quantity_after
        inventory.save(update_fields=["quantity", "updated_at"])

        movement = StockMovement.objects.create(
            inventory=inventory,
            quantity_before=quantity_before,
            quantity=quantity,
            quantity_after=quantity_after,
            movement_type=StockMovementType.RESTOCK,
            reference_type=reference_type,
            reference_id=reference_id,
            reason=reason,
        )

        return inventory, movement

    @staticmethod
    @transaction.atomic
    def remove_stock(
        inventory_id,
        quantity,
        movement_type,
        reason="",
        reference_type="",
        reference_id="",
    ):
        inventory = Inventory.objects.select_for_update().get(id=inventory_id)

        if quantity <= 0:
            raise BadRequestException("Remove quantity must be greater than zero.")

        if movement_type not in StockMovementType.REMOVAL_TYPES:
            raise BadRequestException("Invalid movement type for stock removal.")

        if inventory.quantity < quantity:
            raise BadRequestException("Insufficient stock.")

        quantity_before = inventory.quantity
        quantity_after = quantity_before - quantity

        inventory.quantity = quantity_after
        inventory.save(update_fields=["quantity", "updated_at"])

        movement = StockMovement.objects.create(
            inventory=inventory,
            quantity_before=quantity_before,
            quantity=quantity,
            quantity_after=quantity_after,
            movement_type=movement_type,
            reference_type=reference_type,
            reference_id=reference_id,
            reason=reason,
        )

        LowStockService.check_and_notify(
            inventory=inventory,
            quantity_before=quantity_before,
        )

        return inventory, movement
