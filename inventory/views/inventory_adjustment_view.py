from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.serializers.adjustment_serializer import StockAdjustmentSerializer
from inventory.serializers.inventory_serializer import InventoryDetailSerializer
from inventory.services.inventory_service import InventoryService


class InventoryAdjustmentView(APIView):
    def post(self, request, pk):
        serializer = StockAdjustmentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        inventory, _ = InventoryService.adjust_stock(
            inventory_id=pk,
            **serializer.validated_data,
        )

        return Response(
            InventoryDetailSerializer(inventory).data,
            status=status.HTTP_200_OK,
        )
