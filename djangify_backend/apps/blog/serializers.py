from rest_framework import serializers
from djangify_backend.apps.blog.models import Category, Tag, Post, Comment
from djangify_backend.apps.core.serializers import (
    TimeStampedModelSerializer,
    SEOModelSerializer,
)


class CategorySerializer(TimeStampedModelSerializer, SEOModelSerializer):
    class Meta:
        model = Category
        fields = (
            ["id", "name", "slug", "description"]
            + TimeStampedModelSerializer.Meta.fields
            + SEOModelSerializer.Meta.fields
        )


class TagSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"] + TimeStampedModelSerializer.Meta.fields


class CommentSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "name",
            "email",
            "content",
            "is_approved",
        ] + TimeStampedModelSerializer.Meta.fields
        read_only_fields = ["is_approved"]


class PostSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source="comment_set")

    class Meta:
        model = Post
        fields = (
            [
                "id",
                "title",
                "slug",
                "content",
                "excerpt",
                "featured_image",
                "category",
                "tags",
                "status",
                "published_date",
                "is_featured",
                "comments",
            ]
            + TimeStampedModelSerializer.Meta.fields
            + SEOModelSerializer.Meta.fields
        )
