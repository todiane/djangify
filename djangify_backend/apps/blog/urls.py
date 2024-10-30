from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PostViewSet, CategoryViewSet, TagViewSet, CommentViewSet

router = DefaultRouter()
# Read-only endpoints
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
# Full CRUD endpoints
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    # Nested endpoint for post comments
    path(
        "posts/<slug:post_slug>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="post-comments",
    ),
]
