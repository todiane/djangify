from rest_framework import serializers
from djangify_backend.apps.portfolio.models import Technology, Portfolio, PortfolioImage
from djangify_backend.apps.core.serializers import (
    TimeStampedModelSerializer,
    SEOModelSerializer,
)


class TechnologySerializer(TimeStampedModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "slug", "icon"] + TimeStampedModelSerializer.Meta.fields


class PortfolioImageSerializer(TimeStampedModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = [
            "id",
            "image",
            "caption",
            "order",
        ] + TimeStampedModelSerializer.Meta.fields


class PortfolioSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    """
    Portfolio serializer that maintains project-based API structure
    """

    technologies = TechnologySerializer(many=True, read_only=True)
    images = PortfolioImageSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = (
            [
                "id",
                "title",
                "slug",
                "description",
                "short_description",
                "featured_image",
                "technologies",
                "project_url",
                "github_url",
                "is_featured",
                "order",
                "images",
            ]
            + TimeStampedModelSerializer.Meta.fields
            + SEOModelSerializer.Meta.fields
        )
