from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("api/v1/inventory/", include("inventory.urls")),
    path("api/v1/reports/", include("reports.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/orders/", include("orders.urls")),
    path("api/v1/authentication/", include("authentication.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/plants/", include("plants.urls")),
    # Admin
    path("admin/", admin.site.urls),

    # API documentation
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
]