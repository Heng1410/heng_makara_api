from rest_framework.generics import ListAPIView, RetrieveAPIView

from inventory.models.inventory import Inventory
from inventory.serializers.inventory_serializer import InventoryDetailSerializer, InventoryListSerializer



class InventoryListView(ListAPIView):
    queryset = Inventory.objects.select_related("plant")
    serializer_class = InventoryListSerializer


class InventoryDetailView(RetrieveAPIView):
    queryset = Inventory.objects.select_related("plant")
    serializer_class = InventoryDetailSerializer