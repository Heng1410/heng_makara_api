import django_filters

from plants.models.plants import Plant


class PlantFilter(django_filters.FilterSet):
    class Meta:
        model = Plant
        fields = [
            "category",
            "is_available",
            "is_featured",
        ]