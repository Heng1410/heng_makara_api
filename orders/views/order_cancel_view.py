from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models.orders import Order
from orders.serializers.orders_serializer import OrderSerializer
from orders.services import OrderService


class OrderCancelView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, pk):
        if request.user.role == "manager":
            order = get_object_or_404(Order, pk=pk)

        else:
            order = get_object_or_404(
                Order,
                pk=pk,
                customer=request.user,
            )

        order = OrderService.cancel_order(order=order)

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
