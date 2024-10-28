from django.db import models
from django.utils.text import slugify
from djangify_backend.apps.core.models import TimeStampedModel, SEOModel, SluggedModel
from django.core.validators import FileExtensionValidator
from djangify_backend.apps.core.utils import validate_svg_file

class PostManager(models.Manager):
    """
    Custom manager for Post model providing common query operations
    and optimized database queries with select_related and prefetch_related.
    """
    def get_queryset(self):
        # Optimize database queries by prefetching related fields
        return super().get_queryset().select_related('category').prefetch_related('tags')
    
    def published(self):
        # Returns all published posts, ordered by publication date
        return self.get_queryset().filter(status='published').order_by('-published_date')
    
    def draft(self):
        # Returns all draft posts, ordered by last update
        return self.get_queryset().filter(status='draft').order_by('-updated_at')
    
    def featured(self):
        # Returns featured posts that are published, ordered by publication date
        return self.published().filter(is_featured=True)
    
    def by_category(self, category_slug):
        # Returns published posts for a specific category
        return self.published().filter(category__slug=category_slug)
    
    def by_tag(self, tag_slug):
        # Returns published posts with a specific tag
        return self.published().filter(tags__slug=tag_slug)
    
    def search(self, query):
        # Searches posts by title, content, or excerpt, returns only published posts
        return self.published().filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(excerpt__icontains=query)
        ).distinct()
    
    def archive(self, year, month=None):
        # Returns posts for a specific year and optional month
        queryset = self.published().filter(published_date__year=year)
        if month:
            queryset = queryset.filter(published_date__month=month)
        return queryset.order_by('-published_date')

class CommentManager(models.Manager):
    """
    Custom manager for Comment model providing filtering methods
    and optimized database queries.
    """
    def get_queryset(self):
        # Optimize database queries by prefetching related post
        return super().get_queryset().select_related('post')
    
    def approved(self):
        # Returns only approved comments
        return self.get_queryset().filter(is_approved=True)
    
    def pending(self):
        # Returns comments pending moderation
        return self.get_queryset().filter(is_approved=False)
    
    def for_post(self, post_slug):
        # Returns approved comments for a specific post
        return self.approved().filter(post__slug=post_slug)

class Category(TimeStampedModel, SluggedModel):
    """
    Category model for organizing blog posts.
    Includes timestamped fields from TimeStampedModel.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']  # Add default ordering

    def __str__(self):
        return self.name

class Tag(TimeStampedModel, SluggedModel):
    """
    Tag model for labeling and organizing blog posts.
    Includes timestamped fields from TimeStampedModel.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']  # Add default ordering

    def __str__(self):
        return self.name

    title = models.CharField(max_length=200)


class Post(TimeStampedModel, SluggedModel, SEOModel):
    """
    Blog post model with SEO and timestamp capabilities.
    Supports draft/published status, categories, tags, and featured posts.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    def validate_image(file):
        # Validate SVG files for security
        if file.content_type == 'image/svg+xml':
            validate_svg_file(file)

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="A short summary of the post")
    featured_image = models.ImageField(
        upload_to='blog',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg']),
            validate_image
        ],
        help_text="Image should be at least 800x600 pixels"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        ordering = ['-published_date', '-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(TimeStampedModel):
    """
    Comment model for blog posts.
    Includes moderation capability via is_approved field.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
