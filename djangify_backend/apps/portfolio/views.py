from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.portfolio.models import Technology, Project
from djangify_backend.apps.portfolio.permissions import IsAdminOrReadOnly
from djangify_backend.apps.portfolio.serializers import (
    TechnologySerializer,
    ProjectSerializer,
)
from .filters import ProjectFilter
from .pagination import CustomPortfolioPagination


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPortfolioPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProjectFilter
    search_fields = ["title", "description", "short_description"]
    ordering_fields = ["created_at", "order", "title"]
    ordering = ["order", "-created_at"]

    def get_queryset(self):
        return (
            Project.objects.all()
            .prefetch_related("technologies", "images")
            .order_by("order", "-created_at")
        )
