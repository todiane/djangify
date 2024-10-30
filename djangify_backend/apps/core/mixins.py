from rest_framework import status
from django.core.exceptions import ValidationError
from .utils import FileHandler
import logging

logger = logging.getLogger(__name__)


class FileHandlingMixin:
    """
    Mixin to add file handling capabilities to ViewSets.
    """

    file_handler_class = FileHandler
    upload_field = "file"  # Default field name for file uploads
    upload_path = "uploads/"  # Default upload path
    allowed_types = None  # Default to None (will use FileHandler defaults)
    max_file_size = None  # Default to None (will use FileHandler defaults)
    # Add image optimization settings
    image_optimize = True  # Whether to optimize images
    image_max_size = (800, 800)  # Maximum image dimensions
    image_quality = 85  # JPEG quality

    def handle_file_upload(self, request, field_name=None, path=None):
        """
        Handle file upload with validation and optimization.

        Args:
            request: The request object containing the file
            field_name: Name of the file field (defaults to self.upload_field)
            path: Upload path (defaults to self.upload_path)

        Returns:
            str: Path to saved file

        Raises:
            ValidationError: If file validation fails
        """
        try:
            field_name = field_name or self.upload_field
            path = path or self.upload_path
            file = request.FILES.get(field_name)

            if not file:
                raise ValidationError(f"No file provided for field '{field_name}'")

            handler = self.file_handler_class()

            # Validate file type and size
            handler.validate_file_type(file, self.allowed_types)
            handler.validate_file_size(file, self.max_file_size)

            # Save and optimize file
            return handler.save_file(file, path)

        except ValidationError as e:
            logger.error(f"File validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"File handling error: {str(e)}")
            raise ValidationError(f"Error handling file upload: {str(e)}")

            # Add optimization parameters
            return handler.save_file(
                file,
                path,
                optimize=self.image_optimize,
                max_size=self.image_max_size,
                quality=self.image_quality,
            )

    def perform_create(self, serializer):
        """Override perform_create to handle file uploads."""
        try:
            # Handle file upload if present
            if self.upload_field in self.request.FILES:
                file_path = self.handle_file_upload(self.request)
                serializer.save(**{self.upload_field: file_path})
            else:
                serializer.save()
        except ValidationError as e:
            raise ValidationError(str(e))

    def perform_update(self, serializer):
        """Override perform_update to handle file uploads."""
        try:
            # Handle file upload if present
            if self.upload_field in self.request.FILES:
                file_path = self.handle_file_upload(self.request)
                serializer.save(**{self.upload_field: file_path})
            else:
                serializer.save()
        except ValidationError as e:
            raise ValidationError(str(e))
