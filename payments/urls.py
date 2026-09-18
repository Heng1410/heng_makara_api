from django.urls import include, path
from rest_framework.routers import DefaultRouter

from payments.views.payment_fail_view import PaymentFailView
from payments.views.payment_pay_view import PaymentPayView
from payments.views.payment_refund_view import PaymentRefundView
from payments.views.payments_view_set import PaymentViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"", PaymentViewSet, basename="payments")


urlpatterns = [
    path(
        "<int:pk>/pay",
        PaymentPayView.as_view(),
        name="payment-pay",
    ),
    path(
        "<int:pk>/fail",
        PaymentFailView.as_view(),
        name="payment-fail",
    ),
    path(
        "<int:pk>/refund",
        PaymentRefundView.as_view(),
        name="payment-refund",
    ),
    path("", include(router.urls)),
]
