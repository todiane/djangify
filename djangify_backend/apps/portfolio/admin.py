# apps/portfolio/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Technology, Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', 
                             obj.image.url)
        return "No image"

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'project_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Number of Projects'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_image_preview', 'is_featured', 
                   'order', 'created_at')
    list_filter = ('is_featured', 'technologies', 'created_at')
    search_fields = ('title', 'description', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)
    inlines = [ProjectImageInline]
    list_editable = ('order', 'is_featured')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Technologies & Links', {
            'fields': ('technologies', 'project_url', 'github_url')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', 
                             obj.featured_image.url)
        return "No image"
    featured_image_preview.short_description = 'Preview'

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image_preview', 'caption', 'order')
    list_filter = ('project',)
    search_fields = ('project__title', 'caption')
    list_editable = ('order',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', 
                             obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'