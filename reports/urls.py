from django.urls import path

from reports.views.order_report_view import OrderReportView
from reports.views.plant_report_view import PlantReportView

urlpatterns = [
    path(
        "orders",
        OrderReportView.as_view(),
        name="order-report",
    ),
    path(
        "plants",
        PlantReportView.as_view(),
        name="plant-report",
    ),
]
