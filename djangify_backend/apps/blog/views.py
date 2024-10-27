from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.blog.models import Category, Tag, Post, Comment
from djangify_backend.apps.blog.permissions import IsAuthorOrReadOnly, CommentPermission
from djangify_backend.apps.blog.serializers import (
    CategorySerializer, 
    TagSerializer, 
    PostSerializer, 
    CommentSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related(
            'category'
        ).prefetch_related('tags', 'comment_set')

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [CommentPermission]
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Comment.objects.filter(
            post__slug=self.kwargs['post_slug'],
            is_approved=True
        ).select_related('post')

