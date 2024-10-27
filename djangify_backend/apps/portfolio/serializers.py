from rest_framework import serializers
from djangify_backend.apps.portfolio.models import Technology, Project, ProjectImage
from djangify_backend.apps.core.serializers import TimeStampedModelSerializer, SEOModelSerializer

class TechnologySerializer(TimeStampedModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'slug', 'icon'] + TimeStampedModelSerializer.Meta.fields

class ProjectImageSerializer(TimeStampedModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order'] + TimeStampedModelSerializer.Meta.fields

class ProjectSerializer(TimeStampedModelSerializer, SEOModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True, source='projectimage_set')
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'featured_image', 'technologies', 'project_url', 'github_url',
            'is_featured', 'order', 'images'
        ] + TimeStampedModelSerializer.Meta.fields + SEOModelSerializer.Meta.fields
