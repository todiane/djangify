from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.core.viewsets import BaseViewSet
from djangify_backend.apps.core.utils import FileHandler
from djangify_backend.apps.core.mixins import FileHandlingMixin
from djangify_backend.apps.portfolio.models import Portfolio, Technology, PortfolioImage
from djangify_backend.apps.portfolio.serializers import (
    PortfolioSerializer,
    TechnologySerializer,
    PortfolioImageSerializer,
)
from djangify_backend.apps.core.throttling import (
    WriteOperationThrottle,
    UserBurstRateThrottle,
    UserSustainedRateThrottle,
)
from djangify_backend.apps.portfolio.permissions import IsAdminOrReadOnly
import logging

logger = logging.getLogger(__name__)


class ProjectViewSet(FileHandlingMixin, BaseViewSet):
    """
    ViewSet for Portfolio model providing full CRUD operations.
    Named ProjectViewSet for API consistency.
    """

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [
        WriteOperationThrottle,
        UserBurstRateThrottle,
        UserSustainedRateThrottle,
    ]

    upload_field = "featured_image"
    upload_path = "portfolio/images/"
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
    cache_key_prefix = "project"  # Keep for API consistency

    def get_queryset(self):
        return super().get_queryset().prefetch_related("technologies", "images")

    @action(detail=True, methods=["post"])
    def toggle_featured(self, request, slug=None):
        """Toggle featured status of a portfolio item."""
        try:
            portfolio = self.get_object()
            portfolio.is_featured = not portfolio.is_featured
            portfolio.save()

            return self.success_response(
                data=ProjectSerializer(portfolio).data,
                message=f"Portfolio {'featured' if portfolio.is_featured else 'unfeatured'} successfully",
            )
        except Exception as e:
            logger.error(f"Error toggling featured status: {str(e)}")
            return self.error_response(message=str(e))


class TechnologyViewSet(BaseViewSet):
    """ViewSet for Technology model."""

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    cache_key_prefix = "technology"
    http_method_names = ["get"]
    throttle_classes = [UserBurstRateThrottle, UserSustainedRateThrottle]

    def get_queryset(self):
        return super().get_queryset().prefetch_related("portfolios")


class PortfolioImageViewSet(FileHandlingMixin, BaseViewSet):
    """
    ViewSet for PortfolioImage model.
    Will be registered as 'project-images' for API consistency.
    """

    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    cache_key_prefix = "portfolio_image"

    upload_field = "image"
    upload_path = "portfolio/gallery/"
    allowed_types = FileHandler.ALLOWED_IMAGE_TYPES
    max_file_size = 10 * 1024 * 1024  # 10MB

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["order"]
    ordering = ["order"]

    def get_queryset(self):
        return super().get_queryset().select_related("portfolio")

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
                    data=PortfolioImageSerializer(image).data,
                    message="Image order updated successfully",
                )
            return self.error_response(message="No order provided")
        except Exception as e:
            logger.error(f"Error reordering image: {str(e)}")
            return self.error_response(message=str(e))
