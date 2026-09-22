import django_filters

from notifications.models.notifications import Notification


class NotificationFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Notification
        fields = [
            "is_read",
            "notification_type",
        ]