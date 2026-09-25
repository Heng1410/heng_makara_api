from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.serializers.inventory_serializer import InventoryDetailSerializer
from inventory.serializers.restock_serializer import RestockSerializer
from inventory.services.inventory_service import InventoryService


class InventoryRestockView(APIView):

    def post(self, request, pk):
        serializer = RestockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inventory, _ = InventoryService.restock(
            inventory_id=pk,
            **serializer.validated_data,
        )

        return Response(
            InventoryDetailSerializer(inventory).data,
            status=status.HTTP_200_OK,
        )
