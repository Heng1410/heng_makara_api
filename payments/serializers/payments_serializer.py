from rest_framework import serializers

from payments.models.payments import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "status",
            "method",
            "transaction_id",
            "paid_at",
            "failure_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "amount",
            "status",
            "transaction_id",
            "paid_at",
            "failure_reason",
            "created_at",
            "updated_at",
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "status",
            "method",
            "paid_at",
            "created_at",
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "status",
            "method",
            "transaction_id",
            "paid_at",
            "failure_reason",
            "created_at",
            "updated_at",
        ]