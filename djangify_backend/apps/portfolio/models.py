from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image
from djangify_backend.apps.core.models import TimeStampedModel, SEOModel, SluggedModel
from djangify_backend.apps.portfolio.utils import (
    optimize_image,
    generate_thumbnail,
    upload_to_project,
    upload_to_project_thumb,
)


# Custom validators for the portfolio app
def validate_project_image(value):
    """Validate project image file size and dimensions."""
    # Define maximum file size (5MB)
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("Image file size must not exceed 5MB.")

    try:
        image = Image.open(value)
        min_width = 800
        min_height = 600
        if image.width < min_width or image.height < min_height:
            raise ValidationError(
                f"Image dimensions must be at least {min_width}x{min_height} pixels."
            )
    except Exception as e:
        raise ValidationError("Invalid image file.")


def validate_github_url(value):
    """Validate that the URL is a GitHub repository URL."""
    if value and not value.startswith(("https://github.com/", "http://github.com/")):
        raise ValidationError(
            "Invalid GitHub URL. URL must start with https://github.com/"
        )


def validate_technology_icon(value):
    """Validate technology icon name."""
    allowed_icons = {"python", "javascript", "react", "django", "nextjs", "typescript"}
    if value not in allowed_icons:
        raise ValidationError(
            f'Invalid icon name. Must be one of: {", ".join(allowed_icons)}'
        )


class ProjectManager(models.Manager):
    """
    Custom manager for Project model providing common query operations
    and optimized database queries.
    """

    def get_queryset(self):
        # Optimize database queries by prefetching related fields
        return super().get_queryset().prefetch_related("technologies", "images")

    def featured(self):
        # Returns featured projects ordered by the order field
        return self.get_queryset().filter(is_featured=True).order_by("order")

    def by_technology(self, technology_slug):
        # Returns projects filtered by technology
        return self.get_queryset().filter(technologies__slug=technology_slug)

    def search(self, query):
        # Searches projects by title, description, or short description
        return (
            self.get_queryset()
            .filter(
                models.Q(title__icontains=query)
                | models.Q(description__icontains=query)
                | models.Q(short_description__icontains=query)
            )
            .distinct()
        )

    def with_github(self):
        # Returns projects that have GitHub links
        return self.get_queryset().exclude(github_url="")

    def with_live_demo(self):
        # Returns projects that have live demo links
        return self.get_queryset().exclude(project_url="")


class ProjectImageManager(models.Manager):
    """
    Custom manager for ProjectImage model providing optimized queries
    and common filtering operations.
    """

    def get_queryset(self):
        # Optimize database queries by selecting related project
        return super().get_queryset().select_related("project")

    def for_project(self, project_slug):
        # Returns all images for a specific project
        return self.get_queryset().filter(project__slug=project_slug)

    def ordered(self):
        # Returns all images ordered by their order field
        return self.get_queryset().order_by("order")


class Technology(TimeStampedModel, SluggedModel):
    """
    Technology model for categorizing project technologies.
    Includes timestamped fields from TimeStampedModel.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(
        max_length=50,
        validators=[validate_technology_icon],
        help_text="Icon name for the technology (e.g., 'python', 'react')",
    )

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(TimeStampedModel, SEOModel, SluggedModel):
    """
    Project model for portfolio projects.
    Includes SEO and timestamp capabilities.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200, help_text="A brief summary of the project"
    )
    featured_image = models.ImageField(
        upload_to=upload_to_project,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_project_image,
        ],
        help_text="Main project image (min 800x600px, max 5MB)",
    )
    thumbnail = models.ImageField(
        upload_to=upload_to_project_thumb,
        blank=True,
        null=True,
        help_text="Automatically generated thumbnail",
    )
    technologies = models.ManyToManyField(Technology, related_name="projects")
    project_url = models.URLField(blank=True, help_text="URL for the live project demo")
    github_url = models.URLField(
        blank=True, validators=[validate_github_url], help_text="GitHub repository URL"
    )
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(
        default=0,
        help_text="Order in which the project appears (lower numbers appear first)",
    )

    objects = ProjectManager()

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)

        if self.featured_image:
            # Optimize the main image
            self.featured_image = optimize_image(self.featured_image)

            # Generate thumbnail if it doesn't exist
            if not self.thumbnail:
                self.thumbnail = generate_thumbnail(self.featured_image)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class ProjectImage(TimeStampedModel):
    """
    ProjectImage model for additional project images.
    Includes ordering capability and image validation.
    """

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="projects",
        null=True,
        blank=True,  # Allow blank in forms
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_project_image,
        ],
        help_text="Additional project image (min 800x600px, max 5MB)",
    )
    caption = models.CharField(max_length=200, help_text="Description of the image")
    order = models.IntegerField(
        default=0,
        help_text="Order in which the image appears (lower numbers appear first)",
    )

    objects = ProjectImageManager()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.project.title}"
