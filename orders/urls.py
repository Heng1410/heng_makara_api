from rest_framework.routers import DefaultRouter
from django.urls import include, path

from orders.views.order_complete_view import OrderCompleteView
from orders.views.orders_view_set import OrderViewSet
from orders.views.order_cancel_view import OrderCancelView
from orders.views.order_confirm_view import OrderConfirmView

router = DefaultRouter(trailing_slash=False)
router.register(r"", OrderViewSet)

urlpatterns = [
    path(
        "<int:pk>/confirm",
        OrderConfirmView.as_view(),
        name="order-confirm",
    ),
    path("<int:pk>/cancel", OrderCancelView.as_view(), name="order-cancel"),
    path(
        "<int:pk>/complete",
        OrderCompleteView.as_view(),
        name="order-complete",
    ),
    path(
        "",
        include(router.urls),
    ),
]
