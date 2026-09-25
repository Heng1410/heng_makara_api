from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from inventory.models.stock_movement import StockMovement
from inventory.serializers.stock_movement_serializer import StockMovementDetailSerializer, StockMovementListSerializer
from inventory.stock_movement_filter import StockMovementFilter


class StockMovementListView(ListAPIView):
    queryset = StockMovement.objects.select_related(
        "inventory",
        "inventory__plant",
    )
    serializer_class = StockMovementListSerializer

    filter_backends = [
        DjangoFilterBackend,
    ]

    filterset_class = StockMovementFilter


class StockMovementDetailView(RetrieveAPIView):
    queryset = StockMovement.objects.select_related(
        "inventory",
        "inventory__plant",
    )

    serializer_class = StockMovementDetailSerializer
