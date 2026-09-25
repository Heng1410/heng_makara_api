from authentication.serializers.authentication_serializer import User
from notifications.services.notifications_service import NotificationService
from users.constants import ROLE_MANAGER


class LowStockService:

    @staticmethod
    def check_and_notify(inventory, quantity_before):
        if not inventory.is_active:
            return

        if inventory.quantity > inventory.low_stock_threshold:
            return

        if quantity_before <= inventory.low_stock_threshold:
            return

        manager = User.objects.filter(
            role=ROLE_MANAGER,
            is_active=True,
        ).first()

        if not manager:
            return

        plant = inventory.plant

        NotificationService.create_notification(
            recipient=manager,
            title="Low Stock",
            message=(
                f"{plant.name} is low in stock. "
                f"Only {inventory.quantity} remaining."
            ),
            notification_type="low_stock",
        )
