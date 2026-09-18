from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models.payments import Payment
from payments.serializers.payments_serializer import (
    PaymentDetailSerializer,
    PaymentListSerializer,
    PaymentSerializer,
)
from payments.services.payments_service import PaymentService


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        if self.request.user.role == "manager":
            return Payment.objects.all()

        return Payment.objects.filter(
            order__customer=self.request.user,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer

        if self.action == "retrieve":
            return PaymentDetailSerializer

        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        payment = PaymentService.create_payment(
            order=serializer.validated_data["order"],
            method=serializer.validated_data["method"],
            customer=request.user,
        )

        response_serializer = PaymentDetailSerializer(payment)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
