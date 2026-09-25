from rest_framework import serializers

from inventory.models.inventory import Inventory


class RestockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    reason = serializers.CharField(required=True, allow_blank=True)
    reference_type = serializers.CharField(required=False, allow_blank=True)
    reference_id = serializers.CharField(required=False, allow_blank=True)
