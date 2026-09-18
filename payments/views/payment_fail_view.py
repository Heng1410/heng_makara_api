from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models.payments import Payment
from payments.serializers.payments_serializer import PaymentDetailSerializer
from payments.services.payments_service import PaymentService


class PaymentFailView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)

        if request.user.role != "manager" and payment.order.customer != request.user:
            return Response(
                {"detail": "You cannot update this payment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        failure_reason = request.data.get("failure_reason")

        if not failure_reason:
            return Response(
                {"detail": "failure_reason is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = PaymentService.mark_as_failed(
            payment=payment, failure_reason=failure_reason
        )

        serializer = PaymentDetailSerializer(payment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
