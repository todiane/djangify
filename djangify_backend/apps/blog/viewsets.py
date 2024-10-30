from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from djangify_backend.apps.core.viewsets import BaseViewSet
from djangify_backend.apps.core.mixins import FileHandlingMixin
from djangify_backend.apps.core.utils import FileHandler
from djangify_backend.apps.blog.models import Post, Category, Tag, Comment
from djangify_backend.apps.blog.serializers import (
    PostSerializer,
    CategorySerializer,
    TagSerializer,
    CommentSerializer,
)
from djangify_backend.apps.blog.permissions import IsAuthorOrReadOnly, CommentPermission
import logging

logger = logging.getLogger(__name__)


class PostViewSet(FileHandlingMixin, BaseViewSet):
    """
    ViewSet for Post model providing full CRUD operations.
    Includes caching, filtering, and search capabilities.
    """

    # Basic configurations
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = "slug"
    cache_key_prefix = "post"

    # File handling configurations
    upload_field = "featured_image"
    upload_path = "blog/images/"
    allowed_types = FileHandler.ALLOWED_IMAGE_TYPES
    max_file_size = 10 * 1024 * 1024  # 10MB

    # Filtering and searching
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category__slug", "tags__slug", "status", "is_featured"]
    search_fields = ["title", "content", "excerpt"]
    ordering_fields = ["created_at", "published_date", "title"]
    ordering = ["-published_date"]

    def get_queryset(self):
        """
        Override to optimize query with select_related and prefetch_related.
        Filters unpublished posts for non-staff users.
        """
        queryset = (
            super()
            .get_queryset()
            .select_related("category")
            .prefetch_related("tags", "comments")
        )

        if not self.request.user.is_staff:
            queryset = queryset.filter(status="published")

        return queryset

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

    @action(detail=True, methods=["POST"])
    def upload_featured_image(self, request, slug=None):
        """Custom action for featured image upload."""
        try:
            file_path = self.handle_file_upload(
                request, field_name="featured_image", path="blog/images/"
            )

            post = self.get_object()
            serializer = self.get_serializer(
                post, data={"featured_image": file_path}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return self.success_response(
                data=serializer.data, message="Featured image uploaded successfully"
            )
        except ValidationError as e:
            return self.error_response(str(e))

    @action(detail=True, methods=["post"])
    def toggle_featured(self, request, slug=None):
        """Toggle featured status of a post."""
        try:
            post = self.get_object()
            post.is_featured = not post.is_featured
            post.save()

            return self.success_response(
                data=PostSerializer(post).data,
                message=f"Post {'featured' if post.is_featured else 'unfeatured'} successfully",
            )
        except Exception as e:
            logger.error(f"Error toggling featured status: {str(e)}")
            return self.error_response(message=str(e))


class CategoryViewSet(BaseViewSet):
    """
    ViewSet for Category model providing list and retrieve operations.
    Includes post count and caching.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]
    cache_key_prefix = "category"
    http_method_names = ["get"]  # Restrict to read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("posts")


class TagViewSet(BaseViewSet):
    """
    ViewSet for Tag model providing list and retrieve operations.
    Includes post count and caching.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    cache_key_prefix = "tag"
    http_method_names = ["get"]  # Restrict to read-only operations

    def get_queryset(self):
        return super().get_queryset().prefetch_related("posts")


class CommentViewSet(BaseViewSet):
    """
    ViewSet for Comment model with moderation support.
    Includes spam detection and approval workflow.
    """

    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["is_approved"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    cache_key_prefix = "comment"

    def get_queryset(self):
        """Filter comments based on user permissions and post."""
        queryset = Comment.objects.select_related("post")

        if self.request.user.is_staff:
            return queryset

        # For non-staff users, only show approved comments
        return queryset.filter(is_approved=True)

    def perform_create(self, serializer):
        """Auto-approve comments from staff users."""
        is_approved = True if self.request.user.is_staff else False
        serializer.save(is_approved=is_approved)

    @action(detail=True, methods=["post"], permission_classes=[CommentPermission])
    def approve(self, request, pk=None):
        """Approve a comment."""
        try:
            comment = self.get_object()
            comment.is_approved = True
            comment.save()

            return self.success_response(
                data=CommentSerializer(comment).data,
                message="Comment approved successfully",
            )
        except Exception as e:
            logger.error(f"Error approving comment: {str(e)}")
            return self.error_response(message=str(e))

    @action(detail=True, methods=["post"], permission_classes=[CommentPermission])
    def reject(self, request, pk=None):
        """Reject a comment."""
        try:
            comment = self.get_object()
            comment.is_approved = False
            comment.save()

            return self.success_response(
                data=CommentSerializer(comment).data,
                message="Comment rejected successfully",
            )
        except Exception as e:
            logger.error(f"Error rejecting comment: {str(e)}")
            return self.error_response(message=str(e))
