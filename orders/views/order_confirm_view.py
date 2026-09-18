from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.permission import IsManager
from orders.serializers.orders_serializer import OrderSerializer
from orders.services import OrderService
from orders.models.orders import Order


class OrderConfirmView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, pk):
        order = get_object_or_404(
            Order,
            pk=pk,
        )

        order = OrderService.confirm_order(order=order)

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)
