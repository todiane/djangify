from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.core.viewsets import BaseViewSet
from djangify_backend.apps.core.utils import FileHandler
from djangify_backend.apps.core.mixins import FileHandlingMixin
from djangify_backend.apps.portfolio.models import Project, Technology, ProjectImage
from django.core.exceptions import ValidationError
from djangify_backend.apps.portfolio.serializers import (
    ProjectSerializer,
    TechnologySerializer,
    ProjectImageSerializer,
)
from djangify_backend.apps.portfolio.permissions import IsAdminOrReadOnly
import logging

logger = logging.getLogger(__name__)


class ProjectViewSet(FileHandlingMixin, BaseViewSet):
    """
    ViewSet for Project model providing full CRUD operations.
    Includes image handling and caching.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]

    # File handling configurations
    upload_field = "featured_image"  # Matches your Project model field
    upload_path = "projects/images/"  # Where project images will be stored
    allowed_types = FileHandler.ALLOWED_IMAGE_TYPES

    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["technologies__slug", "is_featured"]
    search_fields = ["title", "description", "short_description"]
    ordering_fields = ["order", "created_at", "title"]
    ordering = ["order", "-created_at"]
    cache_key_prefix = "project"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("technologies", "images")

    @action(detail=True, methods=["post"])
    def toggle_featured(self, request, slug=None):
        """Toggle featured status of a project."""
        try:
            project = self.get_object()
            project.is_featured = not project.is_featured
            project.save()

            return self.success_response(
                data=ProjectSerializer(project).data,
                message=f"Project {'featured' if project.is_featured else 'unfeatured'} successfully",
            )
        except Exception as e:
            logger.error(f"Error toggling featured status: {str(e)}")
            return self.error_response(message=str(e))

    @action(detail=True, methods=["post"])
    def reorder(self, request, slug=None):
        """Update project display order."""
        try:
            project = self.get_object()
            new_order = request.data.get("order")

            if new_order is not None:
                project.order = new_order
                project.save()

                return self.success_response(
                    data=ProjectSerializer(project).data,
                    message="Project order updated successfully",
                )
            return self.error_response(message="No order provided")
        except Exception as e:
            logger.error(f"Error reordering project: {str(e)}")
            return self.error_response(message=str(e))


class TechnologyViewSet(BaseViewSet):
    """
    ViewSet for Technology model providing list and retrieve operations.
    Includes project count and caching.
    """

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    cache_key_prefix = "technology"
    http_method_names = ["get"]  # Restrict to read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("projects")


class ProjectImageViewSet(FileHandlingMixin, BaseViewSet):
    """
    ViewSet for ProjectImage model with image upload handling.
    Includes image optimization and validation.
    """

    # Basic configurations
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    cache_key_prefix = "project_image"

    # File handling configurations
    upload_field = "image"
    upload_path = "projects/gallery/"
    allowed_types = FileHandler.ALLOWED_IMAGE_TYPES
    max_file_size = 10 * 1024 * 1024  # 10MB

    # Filtering and ordering
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["order"]
    ordering = ["order"]

    def get_queryset(self):
        """Optimize queries with select_related."""
        return super().get_queryset().select_related("project")

    def create(self, request, *args, **kwargs):
        """Override create to handle validation errors."""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return self.error_response(str(e))

    def update(self, request, *args, **kwargs):
        """Override update to handle validation errors."""
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return self.error_response(str(e))

    @action(detail=True, methods=["post"])
    def reorder(self, request, pk=None):
        """Update image display order."""
        try:
            image = self.get_object()
            new_order = request.data.get("order")

            if new_order is not None:
                image.order = new_order
                image.save()

                return self.success_response(
                    data=ProjectImageSerializer(image).data,
                    message="Image order updated successfully",
                )
            return self.error_response(message="No order provided")
        except Exception as e:
            logger.error(f"Error reordering image: {str(e)}")
            return self.error_response(message=str(e))
