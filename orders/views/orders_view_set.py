from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import DecimalField, ExpressionWrapper, F, Sum

from orders.models.orders import Order
from orders.order_filter import OrderFilter
from orders.serializers.orders_serializer import OrderListSerializer, OrderSerializer
from orders.services import OrderService


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    permission_classes = [
        IsAuthenticated,
    ]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = OrderFilter
    ordering_fields = ["created_at", "updated_at", "total"]
    ordering = ["-created_at"]

    def get_queryset(self):
        if self.request.user.role == "manager":
            queryset = Order.objects.all()
        else:
            queryset = self.request.user.orders.all()

        return queryset.annotate(
            total=Sum(
                ExpressionWrapper(
                    F("items__quantity") * F("items__unit_price"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        ).prefetch_related("items__plant")

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderListSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            customer=request.user,
            items=serializer.validated_data["items"],
        )

        response_serializer = OrderSerializer(order)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
