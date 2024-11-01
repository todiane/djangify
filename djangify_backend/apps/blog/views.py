from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

# Local imports
from djangify_backend.apps.core.views import BaseViewSet
from djangify_backend.apps.core.pagination import CustomPagination
from djangify_backend.apps.blog.models import Post, Category, Tag, Comment
from djangify_backend.apps.blog.serializers import (
    PostSerializer,
    CategorySerializer,
    TagSerializer,
    CommentSerializer,
)
from djangify_backend.apps.blog.permissions import IsAuthorOrReadOnly, CommentPermission
from djangify_backend.apps.blog.utils.spam_detection import SpamDetector
from djangify_backend.apps.blog.utils.notifications import NotificationManager
from djangify_backend.apps.blog.filters import PostFilter, CommentFilter


class CategoryViewSet(BaseViewSet):
    """
    ViewSet for Category model providing list and retrieve operations.
    Includes caching and search functionality.
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
    Includes caching and search functionality.
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


class PostViewSet(BaseViewSet):
    """
    ViewSet for Post model providing full CRUD operations.
    Includes filtering, search, and caching capabilities.
    """

    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PostFilter
    search_fields = ["title", "content", "excerpt"]
    ordering_fields = ["created_at", "published_date", "title"]
    ordering = ["-published_date"]
    cache_key_prefix = "post"

    def retrieve(self, request, *args, **kwargs):
        print(f"Retrieving post with slug: {kwargs.get('slug')}")
        instance = self.get_object()
        print(f"Found post: {instance.title}")
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
                "message": "Post retrieved successfully",
            }
        )

    def get_queryset(self):
        """
        Returns published posts for non-staff users,
        all posts for staff users.
        """
        queryset = Post.objects.select_related("category").prefetch_related(
            "tags", "comments"
        )

        if not self.request.user.is_staff:
            queryset = queryset.filter(status="published")

        return queryset


class CommentViewSet(BaseViewSet):
    """
    ViewSet for Comment model with moderation support.
    Includes spam detection, filtering, and notifications.
    """

    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]
    pagination_class = CustomPagination
    filter_class = CommentFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    cache_key_prefix = "comment"

    def get_queryset(self):
        """Filter comments based on user permissions and post."""
        queryset = Comment.objects.select_related("post")

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(is_approved=True)

    def perform_create(self, serializer):
        """
        Create new comment with spam detection
        """
        spam_detector = SpamDetector()
        is_spam, reason = spam_detector.check_comment(
            content=serializer.validated_data["content"],
            email=serializer.validated_data["email"],
            name=serializer.validated_data["name"],
        )

        # Auto-approve comments from staff users
        is_approved = True if self.request.user.is_staff else not is_spam

        comment = serializer.save(is_approved=is_approved)

        # Send notifications
        NotificationManager.send_comment_notification(comment)

        if is_approved:
            NotificationManager.send_comment_approval_notification(comment)
        elif is_spam:
            NotificationManager.send_comment_rejection_notification(comment, reason)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Approve a comment and send notification."""
        comment = self.get_object()
        comment.is_approved = True
        comment.save()

        NotificationManager.send_comment_approval_notification(comment)

        return self.success_response(
            data=CommentSerializer(comment).data,
            message="Comment approved successfully",
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Reject a comment and send notification."""
        comment = self.get_object()
        comment.is_approved = False
        comment.save()

        reason = request.data.get("reason", "Comment was found inappropriate")
        NotificationManager.send_comment_rejection_notification(comment, reason)

        return self.success_response(
            data=CommentSerializer(comment).data,
            message="Comment rejected successfully",
        )
