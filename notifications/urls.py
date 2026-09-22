from django.urls import include, path
from rest_framework.routers import DefaultRouter

from notifications.views.notification_read_all_view import NotificationReadAllView
from notifications.views.notification_read_view import NotificationReadView
from notifications.views.notification_unread_count_view import (
    NotificationUnreadCountView,
)
from notifications.views.notifications_view_set import NotificationViewSet

router = DefaultRouter(trailing_slash=False)
router.register(
    r"",
    NotificationViewSet,
    basename="notifications",
)


urlpatterns = [
    path(
        "<int:pk>/read",
        NotificationReadView.as_view(),
        name="notification-read",
    ),
    path(
        "unread-count",
        NotificationUnreadCountView.as_view(),
        name="notification-unread-count",
    ),
    path(
        "read-all",
        NotificationReadAllView.as_view(),
        name="notification-read-all",
    ),
    path("", include(router.urls)),
]
