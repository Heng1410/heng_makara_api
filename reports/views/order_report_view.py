from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.services.reports_service import ReportService


class OrderReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = ReportService.get_order_summary()

        return Response(summary)
