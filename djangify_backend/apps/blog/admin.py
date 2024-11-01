from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Tag, Comment


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ("title", "category", "status", "created_at", "is_featured")
    list_filter = ("status", "category", "tags", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Content",
            {"fields": ("title", "slug", "content", "excerpt", "featured_image")},
        ),
        ("Categories and Tags", {"fields": ("category", "tags")}),
        ("Publishing", {"fields": ("status", "published_date", "is_featured")}),
        ("SEO", {"fields": ("meta_description",), "classes": ("collapse",)}),
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
