from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProjectViewSet, TechnologyViewSet, ProjectImageViewSet


router = DefaultRouter()
# Full CRUD endpoints
router.register("projects", ProjectViewSet, basename="project")
# Read-only endpoint
router.register("technologies", TechnologyViewSet, basename="technology")
# Image handling endpoint
router.register("project-images", ProjectImageViewSet, basename="project-image")

urlpatterns = router.urls
