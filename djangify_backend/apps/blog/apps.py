from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangify_backend.apps.blog'
    verbose_name = 'Blog'
