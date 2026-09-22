from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models.notifications import Notification
from notifications.serializers.notifications_serializer import NotificationSerializer
from notifications.services.notifications_service import NotificationService


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user,
        )

        notification = NotificationService.mark_as_read(notification=notification)

        serializer = NotificationSerializer(notification)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
