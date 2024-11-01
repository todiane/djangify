from rest_framework import serializers
from djangify_backend.apps.blog.models import Category, Tag, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "post_count",
            "created_at",
            "updated_at",
        ]

    def get_post_count(self, obj):
        return obj.posts.count()


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "post_count", "created_at", "updated_at"]

    def get_post_count(self, obj):
        return obj.posts.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "name",
            "email",
            "content",
            "is_approved",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_approved"]


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    published_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    reading_time = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
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
            "created_at",
            "updated_at",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "comments",
            "reading_time",
            "word_count",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_comments(self, obj):
        comments = obj.comments.filter(is_approved=True)
        return CommentSerializer(comments, many=True).data

    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        minutes = word_count / 200
        return round(minutes) if minutes >= 1 else 1

    def get_word_count(self, obj):
        return len(obj.content.split())

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Add category name for convenience
        if instance.category:
            representation["category_name"] = instance.category.name

        return representation


def to_representation(self, instance):
    representation = super().to_representation(instance)

    # Calculate reading time
    # Average reading speed: 200 words per minute
    word_count = len(instance.content.split())
    minutes = word_count / 200
    if minutes < 1:
        reading_time = "less than a minute"
    elif minutes < 1.5:
        reading_time = "1 minute"
    else:
        reading_time = f"{round(minutes)} minutes"

    # Get comment statistics
    total_comments = instance.comments.filter(is_approved=True).count()

    # Add the new fields to the representation
    representation.update(
        {
            "reading_time": reading_time,
            "word_count": word_count,
            "comment_count": total_comments,
            "category_name": instance.category.name if instance.category else None,
        }
    )

    # Format dates in a more readable way
    if representation.get("published_date"):
        published_date = instance.published_date
        representation["published_date_formatted"] = published_date.strftime(
            "%B %d, %Y"
        )

    return representation
