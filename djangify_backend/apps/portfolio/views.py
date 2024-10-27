from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.portfolio.models import Technology, Project
from djangify_backend.apps.portfolio.permissions import IsAdminOrReadOnly
from djangify_backend.apps.portfolio.serializers import (
    TechnologySerializer,
    ProjectSerializer
)

class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['technologies__slug', 'is_featured']
    search_fields = ['title', 'description', 'short_description']

    def get_queryset(self):
        return Project.objects.all().prefetch_related(
            'technologies', 
            'projectimage_set'
        ).order_by('order')
  
