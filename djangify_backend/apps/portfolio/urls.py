# File: djangify_backend/apps/portfolio/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djangify_backend.apps.portfolio.viewsets import (
    ProjectViewSet,  # Keeping this name for API consistency
    TechnologyViewSet,
    PortfolioImageViewSet,
)

router = DefaultRouter()
# Keep 'projects' URL pattern for API consistency
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"technologies", TechnologyViewSet, basename="technology")
router.register(r"project-images", PortfolioImageViewSet, basename="project-image")

urlpatterns = [
    path("", include(router.urls)),
]
