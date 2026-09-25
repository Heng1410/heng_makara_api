from django.db.models import (
    Avg,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Q,
    Sum,
)
from django.db.models.functions import Coalesce
from django.db.models import Value

from orders.models.orders import Order
from payments.models.payments import Payment
from plants.models.plants import Plant


class ReportService:
    
    @staticmethod
    def get_payment_summary():
        payments = Payment.objects.all()
        

    @staticmethod
    def get_order_summary():
        summary = Order.objects.aggregate(
            total_orders=Count("id"),
            pending_orders=Count("id", filter=Q(status="pending")),
            confirmed_orders=Count("id", filter=Q(status="confirmed")),
            completed_orders=Count("id", filter=Q(status="completed")),
            cancelled_orders=Count("id", filter=Q(status="cancelled")),
        )

        completed_revenue = Order.objects.filter(status="completed").aggregate(
            revenue=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F("items__quantity") * F("items__unit_price"),
                        output_field=DecimalField(
                            max_digits=10,
                            decimal_places=2,
                        ),
                    )
                ),
                Value(
                    0,
                    output_field=DecimalField(
                        max_digits=10,
                        decimal_places=2,
                    ),
                ),
            )
        )["revenue"]

        total_revenue = Order.objects.aggregate(
            revenue=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F("items__quantity") * F("items__unit_price"),
                        output_field=DecimalField(
                            max_digits=10,
                            decimal_places=2,
                        ),
                    )
                ),
                Value(
                    0,
                    output_field=DecimalField(
                        max_digits=10,
                        decimal_places=2,
                    ),
                ),
            )
        )["revenue"]

        orders = Order.objects.annotate(
            order_total=Sum(
                ExpressionWrapper(
                    F("items__quantity") * F("items__unit_price"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )

        average_order_value = orders.aggregate(
            average=Avg("order_total"),
        )["average"]

        summary["completed_revenue"] = completed_revenue
        summary["total_revenue"] = total_revenue
        summary["average_order_value"] = average_order_value

        return summary

    @staticmethod
    def get_plant_summary():
        plants = Plant.objects.all()

        total_plants = plants.count()

        available_plants = plants.filter(
            is_available=True,
        ).count()

        out_of_stock_plants = plants.filter(
            stock_quantity=0,
        ).count()

        total_stock = plants.aggregate(
            total=Sum("stock_quantity"),
        )["total"]

        inventory_value = plants.aggregate(
            total=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F("stock_quantity") * F("estimated_price"),
                        output_field=DecimalField(
                            max_digits=10,
                            decimal_places=2,
                        ),
                    )
                ),
                Value(
                    0,
                    output_field=DecimalField(
                        max_digits=10,
                        decimal_places=2,
                    ),
                ),
            )
        )["total"]

        return {
            "total_plants": total_plants,
            "available_plants": available_plants,
            "out_of_stock_plants": out_of_stock_plants,
            "total_stock": total_stock,
            "inventory_value": inventory_value
        }
