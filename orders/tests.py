from django.test import TestCase
from rest_framework.exceptions import ValidationError

from orders.constants import (
    ORDER_STATUS_CANCELLED,
    ORDER_STATUS_COMPLETED,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_PENDING,
)
from orders.models.order_item import OrderItem
from orders.models.orders import Order
from orders.services import OrderService
from plants.models.plants import Plant
from users.models import User


class OrderServiceTestCase(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="password123",
        )

        self.plant = Plant.objects.create(
            name="Monstera",
            scientific_name="Monstera deliciosa",
            estimated_price=25.00,
            stock_quantity=10,
            is_available=True,
        )

    # ---------------------------------------------------------
    # CREATE ORDER
    # ---------------------------------------------------------

    def test_create_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 2,
                }
            ],
        )

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, ORDER_STATUS_PENDING)

        item = order.items.first()

        self.assertEqual(item.plant, self.plant)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(
            item.unit_price,
            self.plant.estimated_price,
        )

    def test_create_order_without_price(self):
        self.plant.estimated_price = None
        self.plant.save()

        with self.assertRaises(ValidationError):
            OrderService.create_order(
                customer=self.customer,
                items=[
                    {
                        "plant": self.plant,
                        "quantity": 1,
                    }
                ],
            )

        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

    # ---------------------------------------------------------
    # CONFIRM ORDER
    # ---------------------------------------------------------

    def test_confirm_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 2,
                }
            ],
        )

        OrderService.confirm_order(order)

        order.refresh_from_db()
        self.plant.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_CONFIRMED,
        )

        self.assertEqual(
            self.plant.stock_quantity,
            8,
        )

    def test_confirm_order_not_enough_stock(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 11,
                }
            ],
        )

        with self.assertRaises(ValidationError):
            OrderService.confirm_order(order)

        order.refresh_from_db()
        self.plant.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_PENDING,
        )

        self.assertEqual(
            self.plant.stock_quantity,
            10,
        )

    def test_confirm_unavailable_plant(self):
        self.plant.is_available = False
        self.plant.save()

        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        with self.assertRaises(ValidationError):
            OrderService.confirm_order(order)

        order.refresh_from_db()
        self.plant.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_PENDING,
        )

        self.assertEqual(
            self.plant.stock_quantity,
            10,
        )

    def test_confirm_non_pending_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        order.status = ORDER_STATUS_CANCELLED
        order.save()

        with self.assertRaises(ValidationError):
            OrderService.confirm_order(order)

    # ---------------------------------------------------------
    # CANCEL ORDER
    # ---------------------------------------------------------

    def test_cancel_pending_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 2,
                }
            ],
        )

        OrderService.cancel_order(order)

        order.refresh_from_db()
        self.plant.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_CANCELLED,
        )

        # Stock was never deducted because order was pending.
        self.assertEqual(
            self.plant.stock_quantity,
            10,
        )

    def test_cancel_confirmed_order_restores_stock(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 2,
                }
            ],
        )

        OrderService.confirm_order(order)

        self.plant.refresh_from_db()

        self.assertEqual(
            self.plant.stock_quantity,
            8,
        )

        OrderService.cancel_order(order)

        order.refresh_from_db()
        self.plant.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_CANCELLED,
        )

        self.assertEqual(
            self.plant.stock_quantity,
            10,
        )

    def test_cancel_completed_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        OrderService.confirm_order(order)
        OrderService.complete_order(order)

        with self.assertRaises(ValidationError):
            OrderService.cancel_order(order)

    def test_cancel_already_cancelled_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        OrderService.cancel_order(order)

        with self.assertRaises(ValidationError):
            OrderService.cancel_order(order)

    # ---------------------------------------------------------
    # COMPLETE ORDER
    # ---------------------------------------------------------

    def test_complete_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 2,
                }
            ],
        )

        OrderService.confirm_order(order)
        OrderService.complete_order(order)

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_COMPLETED,
        )

    def test_complete_pending_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        with self.assertRaises(ValidationError):
            OrderService.complete_order(order)

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_PENDING,
        )

    def test_complete_cancelled_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        OrderService.cancel_order(order)

        with self.assertRaises(ValidationError):
            OrderService.complete_order(order)

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            ORDER_STATUS_CANCELLED,
        )

    def test_complete_already_completed_order(self):
        order = OrderService.create_order(
            customer=self.customer,
            items=[
                {
                    "plant": self.plant,
                    "quantity": 1,
                }
            ],
        )

        OrderService.confirm_order(order)
        OrderService.complete_order(order)

        with self.assertRaises(ValidationError):
            OrderService.complete_order(order)