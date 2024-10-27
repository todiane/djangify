# apps/portfolio/models.py

from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Technology(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(
        max_length=50,
        help_text="Icon identifier (e.g., for Font Awesome or custom icons)"
    )
    
    class Meta:
        verbose_name_plural = "technologies"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200,
        help_text="Brief summary for project cards"
    )
    featured_image = models.ImageField(
        upload_to="portfolio/images/%Y/%m/",
        help_text="Main project image"
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="projects"
    )
    project_url = models.URLField(
        blank=True,
        help_text="Link to live project"
    )
    github_url = models.URLField(
        blank=True,
        help_text="Link to GitHub repository"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Display this project prominently"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["order", "-created_at"]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to="portfolio/images/%Y/%m/",
        help_text="Additional project image"
    )
    caption = models.CharField(max_length=200)
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers first)"
    )
    
    class Meta:
        ordering = ["order"]
    
    def __str__(self):
        return f"Image {self.order} for {self.project.title}"
    