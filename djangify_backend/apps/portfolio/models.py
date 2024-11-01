from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import re
from django.core.validators import FileExtensionValidator
from django.conf import settings
from djangify_backend.apps.core.models import TimeStampedModel, SEOModel
import os
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def validate_portfolio_image(image):
    """
    Validate image file size, dimensions, and format
    """
    # Check file size
    if image.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"Image file too large. Maximum size is {settings.MAX_UPLOAD_SIZE/1024/1024}MB"
        )

    # Check file format
    try:
        with Image.open(image) as img:
            if img.format.upper() not in settings.IMAGE_OPTIMIZATION["FORMATS"]:
                raise ValidationError(
                    f"Unsupported image format. Allowed formats are: {', '.join(settings.IMAGE_OPTIMIZATION['FORMATS'])}"
                )
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        raise ValidationError(
            "Invalid image file. Please ensure the file is a valid image."
        )


def portfolio_image_path(instance, filename):
    """
    Generate upload path for portfolio's featured image
    """
    ext = filename.split(".")[-1]
    filename = f"{instance.slug}.{ext}"
    return os.path.join("portfolio", filename)


def portfolio_gallery_image_path(instance, filename):
    """
    Generate upload path for portfolio gallery images
    """
    ext = filename.split(".")[-1]
    filename = f"{instance.portfolio.slug}-{instance.order}.{ext}"
    return os.path.join("portfolio", "gallery", filename)


def validate_github_url(value):
    """
    Validate that the URL is a valid GitHub repository URL
    """
    github_url_pattern = re.compile(
        r"^(https?://)?(www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$"
    )
    if not github_url_pattern.match(value):
        raise ValidationError("Please enter a valid GitHub repository URL")


def validate_technology_icon(value):
    """
    Validate technology icon format and source
    """
    allowed_formats = ["svg", "png"]
    if not any(value.lower().endswith(f".{fmt}") for fmt in allowed_formats):
        raise ValidationError(
            f"Icon must be one of these formats: {', '.join(allowed_formats)}"
        )


class Technology(TimeStampedModel):
    """
    Model representing a technology/skill used in portfolio projects
    """

    name = models.CharField(
        max_length=100,
        null=True,
        help_text="Name of the technology (e.g., Python, React, Django)",
    )
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the name")
    icon = models.CharField(
        max_length=50,
        help_text="Icon identifier or URL for the technology",
        validators=[validate_technology_icon],
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Portfolio(TimeStampedModel, SEOModel):
    """
    Model representing a portfolio project with detailed information
    """

    title = models.CharField(
        max_length=200,
        default="Default Title",
        help_text="Title of the portfolio project",
    )
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    description = models.TextField(help_text="Detailed description of the project")
    short_description = models.CharField(
        max_length=200, help_text="Brief summary of the project"
    )
    featured_image = models.ImageField(
        upload_to=portfolio_image_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_portfolio_image,
        ],
        help_text="Upload a JPG or PNG image (max 5MB)",
        null=True,
        blank=True,
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="portfolios",
        help_text="Technologies used in this project",
    )
    project_url = models.URLField(
        blank=True, help_text="Live project URL (if available)"
    )
    github_url = models.URLField(
        blank=True, validators=[validate_github_url], help_text="GitHub repository URL"
    )
    is_featured = models.BooleanField(
        default=False, help_text="Display this project in featured sections"
    )
    order = models.IntegerField(
        default=0, help_text="Display order in the portfolio list"
    )

    def clean(self):
        """
        Custom validation for the model
        """
        super().clean()
        if self.featured_image:
            validate_portfolio_image(self.featured_image)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        # Process the image after save if it exists
        if self.featured_image:
            try:
                img = Image.open(self.featured_image.path)

                # Convert image to RGB if it's not
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Resize image if larger than maximum dimensions
                max_size = settings.IMAGE_OPTIMIZATION["MAX_DIMENSION"]
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save optimized image
                img.save(
                    self.featured_image.path,
                    quality=settings.IMAGE_OPTIMIZATION["QUALITY"],
                    optimize=True,
                )
            except Exception as e:
                logger.error(
                    f"Error processing image for portfolio {self.title}: {str(e)}"
                )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title


class PortfolioImage(TimeStampedModel):
    """
    Model representing additional images for a portfolio project
    """

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Portfolio project this image belongs to",
        null=True,
    )
    image = models.ImageField(
        upload_to=portfolio_gallery_image_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_portfolio_image,
        ],
        help_text="Additional project image (JPG or PNG)",
        null=True,
        blank=True,
    )
    caption = models.CharField(max_length=200, help_text="Description of the image")
    order = models.IntegerField(default=0, help_text="Display order in the gallery")

    def clean(self):
        """
        Custom validation for the model
        """
        super().clean()
        if self.image:
            validate_portfolio_image(self.image)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Process the image after save
        if self.image:
            try:
                img = Image.open(self.image.path)

                # Convert image to RGB if it's not
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Resize image if larger than maximum dimensions
                max_size = settings.IMAGE_OPTIMIZATION["MAX_DIMENSION"]
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save optimized image
                img.save(
                    self.image.path,
                    quality=settings.IMAGE_OPTIMIZATION["QUALITY"],
                    optimize=True,
                )
            except Exception as e:
                logger.error(
                    f"Error processing image for portfolio image {self.id}: {str(e)}"
                )

    class Meta:
        ordering = ["order"]
        verbose_name = "Portfolio Image"
        verbose_name_plural = "Portfolio Images"

    def __str__(self):
        return f"Image for {self.portfolio.title}"
