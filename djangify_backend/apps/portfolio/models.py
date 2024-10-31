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


def validate_project_image(image):
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


def project_image_path(instance, filename):
    """
    Generate upload path for project images
    """
    # Get the file extension
    ext = filename.split(".")[-1]
    # Create a new filename using the project slug
    filename = f"{instance.slug}.{ext}"
    return os.path.join("projects", filename)


def validate_github_url(value):
    github_url_pattern = re.compile(
        r"^(https?://)?(www\.)?github\.com/[A-Za-z0-9_.-]+/?$"
    )
    if not github_url_pattern.match(value):
        raise ValidationError(f"{value} is not a valid GitHub URL")


def validate_technology_icon(value):
    icon_url_pattern = re.compile(
        r"^(https?://)?(www\.)?example\.com/icons/[A-Za-z0-9_.-]+\.svg$"
    )
    if not icon_url_pattern.match(value):
        raise ValidationError(f"{value} is not a valid technology icon URL")


class Technology(TimeStampedModel):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ["name"]  # Add default ordering by name

    def __str__(self):
        return self.name


def project_image_path(instance, filename):
    """
    Generate upload path for project's featured image
    """
    ext = filename.split(".")[-1]
    filename = f"{instance.slug}.{ext}"
    return os.path.join("projects", filename)


def project_gallery_image_path(instance, filename):
    """
    Generate upload path for project gallery images
    """
    ext = filename.split(".")[-1]
    # Use project slug and a unique identifier for gallery images
    filename = f"{instance.project.slug}-{instance.order}.{ext}"
    return os.path.join("projects", "gallery", filename)


class Project(TimeStampedModel, SEOModel):
    title = models.CharField(max_length=200, default="Default Title")
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    featured_image = models.ImageField(
        upload_to=project_image_path,  # Use project_image_path for featured image
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_project_image,
        ],
        help_text="Upload a JPG or PNG image (max 5MB)",
        null=True,
        blank=True,
    )
    technologies = models.ManyToManyField(Technology, related_name="projects")
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def clean(self):
        """
        Custom validation for the model
        """
        super().clean()
        if self.featured_image:
            validate_project_image(self.featured_image)

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
                    f"Error processing image for project {self.title}: {str(e)}"
                )

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=project_gallery_image_path,  # Note the updated function name
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_project_image,
        ],
        null=True,
        blank=True,
    )
    caption = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def clean(self):
        super().clean()
        if self.image:
            validate_project_image(self.image)

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
                    f"Error processing image for project image {self.id}: {str(e)}"
                )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.project.title}"
