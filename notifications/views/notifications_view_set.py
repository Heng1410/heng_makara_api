from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from notifications.models.notifications import Notification
from notifications.notification_filter import NotificationFilter
from notifications.serializers.notifications_serializer import (
    NotificationDetailSerializer,
    NotificationListSerializer,
    NotificationSerializer,
)


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotificationFilter

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return NotificationListSerializer

        if self.action == "retrieve":
            return NotificationDetailSerializer

        return NotificationSerializer
