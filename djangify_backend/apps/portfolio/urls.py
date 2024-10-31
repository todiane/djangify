from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProjectViewSet, TechnologyViewSet, ProjectImageViewSet


router = DefaultRouter()
# Full CRUD endpoints
router.register(r"projects", ProjectViewSet, basename="project")
# Read-only endpoint
router.register(r"technologies", TechnologyViewSet, basename="technology")
# Image handling endpoint
router.register(r"project-images", ProjectImageViewSet, basename="project-image")

urlpatterns = [
    path("", include(router.urls)),
]
