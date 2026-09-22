from django.utils import timezone

from notifications.models.notifications import Notification


class NotificationService:

    @staticmethod
    def create_notification(recipient, title, message, notification_type):
        notification = Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
        )

        return notification

    @staticmethod
    def mark_as_read(notification):
        if notification.is_read:
            return notification

        notification.is_read = True
        notification.read_at = timezone.now()

        notification.save(
            update_fields=[
                "is_read",
                "read_at",
                "updated_at",
            ]
        )

        return notification

    @staticmethod
    def mark_all_as_read(user):
        unread_notification = Notification.objects.filter(
            recipient=user,
            is_read=False,
        )

        updated_count = unread_notification.update(
            is_read=True,
            read_at=timezone.now(),
        )

        return updated_count
