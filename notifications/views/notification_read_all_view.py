from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.services.notifications_service import NotificationService


class NotificationReadAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated_count = NotificationService.mark_all_as_read(user=request.user)

        return Response(
            {
                "updated_count": updated_count,
            },
            status=status.HTTP_200_OK,
        )
