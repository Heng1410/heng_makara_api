from rest_framework.routers import DefaultRouter
from django.urls import include, path

from plants.views.plants_view_set import PlantViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r"", PlantViewSet)

urlpatterns = [path("", include(router.urls))]
