from django.db import transaction

from rest_framework.exceptions import ValidationError

from orders.constants import (
    ORDER_STATUS_CANCELLED,
    ORDER_STATUS_COMPLETED,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_PENDING,
)
from orders.models.order_item import OrderItem
from orders.models.orders import Order


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(customer, items):
        for item in items:
            plant = item["plant"]

            if plant.estimated_price is None:
                raise ValidationError(f"{plant.name} does not have a price.")
        order = Order.objects.create(
            customer=customer,
        )

        for item in items:
            plant = item["plant"]

            OrderItem.objects.create(
                order=order,
                plant=plant,
                quantity=item["quantity"],
                unit_price=plant.estimated_price,
            )

        return order

    @staticmethod
    @transaction.atomic
    def confirm_order(order):
        if order.status != ORDER_STATUS_PENDING:
            raise ValidationError("Only pending orders can be confirmed.")

        for item in order.items.select_related("plant").select_for_update():
            plant = item.plant

            if not plant.is_available:
                raise ValidationError(f"{plant.name} is not available.")

            if plant.stock_quantity < item.quantity:
                raise ValidationError(f"Not enough stock for {plant.name}.")

            plant.stock_quantity -= item.quantity

            plant.save(update_fields=["stock_quantity", "updated_at"])

        order.status = ORDER_STATUS_CONFIRMED

        order.save(
            update_fields=["status", "updated_at"],
        )

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order):
        if order.status not in [
            ORDER_STATUS_PENDING,
            ORDER_STATUS_CONFIRMED,
        ]:
            raise ValidationError("Only pending orders can be cancelled.")

        if order.status == ORDER_STATUS_CONFIRMED:
            for item in order.items.select_related("plant").select_for_update():
                plant = item.plant

                plant.stock_quantity += item.quantity

                plant.save(update_fields=["stock_quantity", "updated_at"])

        order.status = ORDER_STATUS_CANCELLED

        order.save(update_fields=["status", "updated_at"])

        return order

    @staticmethod
    @transaction.atomic
    def complete_order(order):
        if order.status != ORDER_STATUS_CONFIRMED:
            raise ValidationError("Only confirmed orders can be completed.")

        order.status = ORDER_STATUS_COMPLETED
        order.save(
            update_fields=["status", "updated_at"],
        )

        return order
