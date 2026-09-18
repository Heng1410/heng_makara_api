from rest_framework.decorators import action

from rest_framework import status, viewsets
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from plants.filters import PlantFilter
from plants.models.plants import Plant
from plants.serializers.plant_image_serializer import PlantImageSerializer
from plants.serializers.plants_serializer import (
    PlantDetailSerializer,
    PlantListSerializer,
    PlantSerializer,
)


class PlantViewSet(viewsets.ModelViewSet):
    model = Plant
    queryset = Plant.objects.all()

    filter_backends = [
        DjangoFilterBackend,
    ]

    filterset_class = PlantFilter

    search_fields = [
        "name",
        "scientific_name",
        "description",
    ]

    ordering_fields = [
        "name",
        "estimated_price",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return PlantListSerializer

        if self.action == "retrieve":
            return PlantDetailSerializer

        return PlantSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="images",
    )
    def upload_image(self, request, pk=None):
        plant = self.get_object()

        serializer = PlantImageSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        image = serializer.save(
            plant=plant,
        )

        return Response(
            PlantImageSerializer(image).data,
            status=status.HTTP_201_CREATED,
        )