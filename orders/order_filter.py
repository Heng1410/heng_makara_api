import django_filters

from orders.models.orders import Order


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [
            "status",
        ]