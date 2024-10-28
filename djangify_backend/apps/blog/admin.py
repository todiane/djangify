from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Tag, Comment

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    
    list_display = ('title', 'display_featured_image', 'category', 'status', 
                   'published_date', 'is_featured', 'created_at')
    list_filter = ('status', 'category', 'tags', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('Post Content', {
            'fields': (
                'title', 
                'slug', 
                'excerpt',
                'content',
            )
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Organization', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'published_date', 'is_featured'),
            'classes': ('collapse',)
        }),
    )
    
    def display_featured_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.featured_image.url
            )
        return "No Image"
    display_featured_image.short_description = 'Image'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content', 'post__title')
    actions = ['approve_comments', 'unapprove_comments']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'name', 'email', 'content')
        }),
        ('Moderation', {
            'fields': ('is_approved',),
            'classes': ('collapse',)
        }),
    )
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments have been approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments have been unapproved.')
    unapprove_comments.short_description = "Unapprove selected comments"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new comments
            obj.is_approved = False  # Set default to unapproved
        super().save_model(request, obj, form, change)
    