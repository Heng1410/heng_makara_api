from rest_framework import serializers

from notifications.models.notifications import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "title",
            "message",
            "notification_type",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "recipient",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "is_read",
            "created_at",
        ]


class NotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "title",
            "message",
            "notification_type",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]