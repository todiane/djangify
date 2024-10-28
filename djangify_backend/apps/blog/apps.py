from django.apps import AppConfig
from django.contrib import admin

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangify_backend.apps.blog'
    verbose_name = 'Blog Management'

    def ready(self):
        # Customize admin site
        admin.site.site_header = 'Djangify Admin'
        admin.site.site_title = 'Djangify Admin Portal'
        admin.site.index_title = 'Welcome to Djangify Admin Portal'
