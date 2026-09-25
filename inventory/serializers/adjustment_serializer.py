from rest_framework import serializers


class StockAdjustmentSerializer(serializers.Serializer):

    quantity = serializers.IntegerField()

    reason = serializers.CharField(required=True, allow_blank=True)

    reference_type = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    reference_id = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
