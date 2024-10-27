from django.db import models
from django.utils.text import slugify
from djangify_backend.apps.core.models import TimeStampedModel, SEOModel
from django.core.validators import FileExtensionValidator
from apps.core.utils import validate_svg_file

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(TimeStampedModel, SEOModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    def validate_image(file):
        if file.content_type == 'image/svg+xml':
            validate_svg_file(file)

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(
        upload_to='blog',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg']),
            validate_image
        ]
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
        