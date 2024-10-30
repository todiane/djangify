from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Post, Comment


class PostFilter(filters.FilterSet):
    """
    Custom filter set for Post model with advanced filtering options
    """

    # Date-based filters
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")
    published_after = filters.DateFilter(field_name="published_date", lookup_expr="gte")
    published_before = filters.DateFilter(
        field_name="published_date", lookup_expr="lte"
    )

    # Tag and category filters
    tags = filters.CharFilter(method="filter_tags")
    category = filters.CharFilter(field_name="category__slug")

    # Text search
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Post
        fields = ["status", "is_featured"]

    def filter_tags(self, queryset, name, value):
        tag_slugs = value.split(",")
        return queryset.filter(tags__slug__in=tag_slugs).distinct()

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(content__icontains=value)
            | Q(excerpt__icontains=value)
        ).distinct()


class CommentFilter(filters.FilterSet):
    """
    Custom filter set for Comment model
    """

    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")
    post = filters.CharFilter(field_name="post__slug")

    class Meta:
        model = Comment
        fields = ["is_approved"]
