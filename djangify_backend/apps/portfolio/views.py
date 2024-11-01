from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.portfolio.models import Technology, Portfolio, PortfolioImage
from djangify_backend.apps.portfolio.serializers import (
    TechnologySerializer,
    PortfolioSerializer,
    PortfolioImageSerializer,
)
from djangify_backend.apps.portfolio.permissions import IsAdminOrReadOnly


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering = ["name"]


class ProjectViewSet(viewsets.ModelViewSet):  # Keep ViewSet name for API consistency
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PortfolioSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["technologies__slug", "is_featured"]
    search_fields = ["title", "description", "short_description"]

    def get_queryset(self):
        return (
            Portfolio.objects.all()
            .prefetch_related("technologies", "images")
            .order_by("order")
        )


class PortfolioImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
