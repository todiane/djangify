from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def upload_to_project(instance, filename):
    """
    Custom function to determine upload path for project images.
    Creates path like: projects/project-slug/filename
    """
    return f"projects/{instance.slug}/{filename}"


def upload_to_project_thumb(instance, filename):
    """
    Custom function to determine upload path for project thumbnails.
    Creates path like: projects/project-slug/thumbnails/filename
    """
    return f"projects/{instance.slug}/thumbnails/{filename}"


def optimize_image(image, max_size=(800, 800), quality=85):
    """
    Optimize uploaded images by resizing and compressing them.
    """
    if not image:
        return None

    img = Image.open(image)

    # Convert to RGB if image is in RGBA mode
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # Calculate new dimensions while maintaining aspect ratio
    ratio = min(max_size[0] / img.width, max_size[1] / img.height)
    new_size = (int(img.width * ratio), int(img.height * ratio))

    if img.width > max_size[0] or img.height > max_size[1]:
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Save the optimized image
    output = BytesIO()
    img.save(output, format="JPEG", quality=quality, optimize=True)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        "ImageField",
        f"{image.name.split('.')[0]}.jpg",
        "image/jpeg",
        sys.getsizeof(output),
        None,
    )


def generate_thumbnail(image, size=(200, 200)):
    """
    Generate a thumbnail from the original image.
    """
    if not image:
        return None

    img = Image.open(image)

    # Convert to RGB if image is in RGBA mode
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # Create thumbnail
    img.thumbnail(size, Image.Resampling.LANCZOS)

    # Save the thumbnail
    output = BytesIO()
    img.save(output, format="JPEG", quality=85, optimize=True)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        "ImageField",
        f"thumb_{image.name.split('.')[0]}.jpg",
        "image/jpeg",
        sys.getsizeof(output),
        None,
    )
