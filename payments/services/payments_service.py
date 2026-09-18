from django.utils import timezone

from django.db import transaction
from rest_framework.exceptions import ValidationError

from orders.constants import ORDER_STATUS_CONFIRMED, ORDER_STATUS_PENDING
from payments.constants import (
    PAYMENT_STATUS_FAILED,
    PAYMENT_STATUS_PAID,
    PAYMENT_STATUS_PENDING,
    PAYMENT_STATUS_REFUNDED,
)
from payments.models.payments import Payment


class PaymentService:

    @staticmethod
    @transaction.atomic
    def create_payment(order, method, customer):
        if hasattr(order, "payment"):
            raise ValidationError("This order already has a payment.")

        if order.customer != customer:
            raise ValidationError("You cannot pay for this order.")

        amount = sum(item.quantity * item.unit_price for item in order.items.all())

        if order.status not in [
            ORDER_STATUS_PENDING,
            ORDER_STATUS_CONFIRMED,
        ]:
            raise ValidationError("This order cannot be paid.")

        payment = Payment.objects.create(
            order=order,
            amount=amount,
            method=method,
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_as_paid(payment):
        if payment.status != PAYMENT_STATUS_PENDING:
            raise ValidationError("Only pending payments can be marked as paid.")

        payment.status = PAYMENT_STATUS_PAID
        payment.paid_at = timezone.now()

        payment.save(update_fields=["status", "paid_at", "updated_at"])

        order = payment.order

        if order.status == ORDER_STATUS_PENDING:
            order.status = ORDER_STATUS_CONFIRMED
            order.save(update_fields=["status", "updated_at"])

        return payment

    @staticmethod
    @transaction.atomic
    def mark_as_failed(payment, failure_reason):
        if payment.status != PAYMENT_STATUS_PENDING:
            raise ValidationError("Only pending payments can be marked as failed.")

        payment.status = PAYMENT_STATUS_FAILED
        payment.failure_reason = failure_reason

        payment.save(update_fields=["status", "failure_reason", "updated_at"])

        return payment

    @staticmethod
    @transaction.atomic
    def mark_as_refunded(payment):
        if payment.status != PAYMENT_STATUS_PAID:
            raise ValidationError("Only paid payments can be refunded.")

        payment.status = PAYMENT_STATUS_REFUNDED

        payment.save(update_fields=["status", "updated_at"])

        return payment
