from rest_framework import serializers
from djangify_backend.apps.core.models import TimeStampedModel, SEOModel

class TimeStampedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStampedModel
        fields = ['created_at', 'updated_at']

class SEOModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOModel
        fields = ['meta_title', 'meta_description', 'meta_keywords']
        