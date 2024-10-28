from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import re
from typing import Optional
from datetime import datetime

# =====================================
# Core Validators
# =====================================

def validate_future_datetime(value: datetime) -> None:
    """
    Ensures a datetime value is in the future.
    Used for scheduling content publication.
    """
    if value < timezone.now():
        raise ValidationError("Datetime must be in the future")

def validate_slug(value: str) -> None:
    """
    Validates slug format:
    - Only lowercase letters, numbers, hyphens
    - Must start and end with letter/number
    - Length between 3-100 characters
    """
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', value):
        raise ValidationError(
            "Slug must contain only lowercase letters, numbers, and hyphens, "
            "and must start and end with a letter or number"
        )
    if len(value) < 3:
        raise ValidationError("Slug must be at least 3 characters long")
    if len(value) > 100:
        raise ValidationError("Slug must be no more than 100 characters long")

def validate_meta_title(value: Optional[str]) -> None:
    """
    Validates SEO meta title:
    - Length between 10-60 characters
    - No excessive whitespace
    """
    if value:
        value = value.strip()
        if len(value) < 10:
            raise ValidationError("Meta title must be at least 10 characters long")
        if len(value) > 60:
            raise ValidationError("Meta title must be no more than 60 characters long")
        if re.search(r'\s{2,}', value):
            raise ValidationError("Meta title cannot contain excessive whitespace")

def validate_meta_description(value: Optional[str]) -> None:
    """
    Validates SEO meta description:
    - Length between 50-160 characters
    - No excessive whitespace
    """
    if value:
        value = value.strip()
        if len(value) < 50:
            raise ValidationError("Meta description must be at least 50 characters long")
        if len(value) > 160:
            raise ValidationError("Meta description must be no more than 160 characters long")
        if re.search(r'\s{2,}', value):
            raise ValidationError("Meta description cannot contain excessive whitespace")

def validate_meta_keywords(value: Optional[str]) -> None:
    """
    Validates SEO meta keywords:
    - Maximum 10 keywords
    - Each keyword between 2-30 characters
    - Only letters, numbers, spaces, hyphens
    """
    if value:
        keywords = [k.strip() for k in value.split(',')]
        if len(keywords) > 10:
            raise ValidationError("No more than 10 meta keywords are allowed")
        for keyword in keywords:
            if len(keyword) < 2:
                raise ValidationError("Each meta keyword must be at least 2 characters long")
            if len(keyword) > 30:
                raise ValidationError("Each meta keyword must be no more than 30 characters long")
            if not re.match(r'^[a-zA-Z0-9\s-]+$', keyword):
                raise ValidationError("Meta keywords can only contain letters, numbers, spaces, and hyphens")

# =====================================
# Mixins
# =====================================

class SlugMixin:
    """
    Mixin that provides automatic slug generation and validation.
    Must be used with a model that has a 'title' field.
    """
    def clean(self):
        super().clean()
        # Generate slug from title if not provided
        if not self.slug and hasattr(self, 'title'):
            self.slug = slugify(self.title)
        if hasattr(self, 'slug'):
            validate_slug(self.slug)

class SEOValidationMixin:
    """
    Mixin that provides validation for SEO fields.
    Must be used with SEOModel.
    """
    def clean(self):
        super().clean()
        if hasattr(self, 'meta_title'):
            validate_meta_title(self.meta_title)
        if hasattr(self, 'meta_description'):
            validate_meta_description(self.meta_description)
        if hasattr(self, 'meta_keywords'):
            validate_meta_keywords(self.meta_keywords)

# =====================================
# Base Models
# =====================================

class TimeStampedModel(models.Model):
    """
    Abstract base model providing automatic timestamps.
    Includes validation to ensure updated_at is not before created_at.
    """
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="The datetime this object was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The datetime this object was last updated"
    )

    def clean(self):
        super().clean()
        # Validate timestamp order
        if self.updated_at and self.created_at and self.updated_at < self.created_at:
            raise ValidationError("Updated timestamp cannot be before creation timestamp")

    class Meta:
        abstract = True

class SEOModel(SEOValidationMixin, models.Model):
    """
    Abstract base model providing SEO fields with validation.
    Includes meta title, description, and keywords with proper validation.
    """
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Maximum 60 characters. Should be unique and descriptive."
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Maximum 160 characters. Provide a concise summary."
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords. Maximum 10 keywords."
    )

    class Meta:
        abstract = True

class SluggedModel(models.Model):
    title = models.CharField(
        max_length=200, 
        null=True, 
        blank=True, 
        default='default_title'  # Add a more meaningful default if needed
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly version of the title. Auto-generated if left blank.",
        default='default-slug'  # Add a default slug as well
    )

    class Meta:
        abstract = True


# =====================================
# Save Hooks
# =====================================

    def save(self, *args, **kwargs):
        """
        Override save method to ensure validation runs before saving.
        This helps catch validation errors even when clean() isn't explicitly called.
        """
        self.full_clean()
        super().save(*args, **kwargs)
