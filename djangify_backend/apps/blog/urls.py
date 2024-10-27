from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djangify_backend.apps.blog.views import (
    CategoryViewSet, 
    TagViewSet, 
    PostViewSet, 
    CommentViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'posts/<slug:post_slug>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='post-comments'
    )
]