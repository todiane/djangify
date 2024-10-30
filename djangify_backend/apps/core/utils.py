import re
from xml.etree import ElementTree
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
from typing import Any, Dict, List, Optional, Tuple, Union
import os
import uuid
import imghdr
import magic
import re
from PIL import Image
from io import BytesIO
import json
import bleach
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ==============================
# File Handling Utilities
# ==============================


class FileHandler:
    """Utility class for file handling operations."""

    ALLOWED_IMAGE_TYPES = {"jpeg", "jpg", "png", "gif", "svg"}
    ALLOWED_DOCUMENT_TYPES = {"pdf", "doc", "docx", "txt", "md"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB default

    @staticmethod
    def generate_unique_filename(filename: str) -> str:
        """Generate a unique filename while preserving extension."""
        name, ext = os.path.splitext(filename)
        return f"{slugify(name)}-{uuid.uuid4().hex[:8]}{ext}"

    @classmethod
    def validate_file_type(cls, file, allowed_types: Optional[set] = None) -> None:
        """
        Validate file type using both extension and mime type.

        Args:
            file: File object to validate
            allowed_types: Set of allowed file extensions

        Raises:
            ValidationError: If file type is not allowed
        """
        if not file:
            return

        # Get file extension
        filename = file.name.lower()
        ext = filename.split(".")[-1] if "." in filename else ""

        # Use provided allowed types or default to image types
        allowed = allowed_types or cls.ALLOWED_IMAGE_TYPES

        if ext not in allowed:
            raise ValidationError(
                f"File type '{ext}' is not allowed. Allowed types: {', '.join(allowed)}"
            )

        # Validate mime type
        try:
            mime = magic.from_buffer(file.read(1024), mime=True)
            file.seek(0)  # Reset file pointer

            if not any(t in mime for t in ["image/", "application/", "text/"]):
                raise ValidationError(f"Invalid file type detected: {mime}")
        except Exception as e:
            logger.error(f"Error validating file type: {str(e)}")
            raise ValidationError("Could not validate file type")

    @classmethod
    def validate_file_size(cls, file, max_size: Optional[int] = None) -> None:
        """
        Validate file size.

        Args:
            file: File object to validate
            max_size: Maximum file size in bytes

        Raises:
            ValidationError: If file is too large
        """
        max_file_size = max_size or cls.MAX_FILE_SIZE
        if file.size > max_file_size:
            raise ValidationError(
                f"File size ({file.size} bytes) exceeds maximum allowed size "
                f"({max_file_size} bytes)"
            )

    @staticmethod
    def optimize_image(
        image_file, max_size: Tuple[int, int] = (800, 800), quality: int = 85
    ) -> BytesIO:
        """
        Optimize image size and quality.

        Args:
            image_file: Image file to optimize
            max_size: Maximum dimensions (width, height)
            quality: JPEG quality (1-100)

        Returns:
            BytesIO: Optimized image data
        """
        img = Image.open(image_file)

        # Convert PNG to RGB if necessary
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background

        # Resize if larger than max_size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save optimized image
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output

    @classmethod
    def save_file(cls, file, path: str, optimize: bool = True) -> str:
        """
        Save file to storage with optimization for images.

        Args:
            file: File to save
            path: Storage path
            optimize: Whether to optimize images

        Returns:
            str: Path to saved file
        """
        try:
            filename = cls.generate_unique_filename(file.name)
            full_path = os.path.join(path, filename)

            # Handle images
            if optimize and imghdr.what(file):
                optimized = cls.optimize_image(file)
                default_storage.save(full_path, ContentFile(optimized.getvalue()))
            else:
                default_storage.save(full_path, file)

            return full_path
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise ValidationError("Failed to save file")


# ==============================
# Data Validation Helpers
# ==============================


class DataValidator:
    """Utility class for data validation."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            bool: True if valid
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            bool: True if valid
        """
        pattern = r"https?://(?:[\w-]+\.)+[\w-]+(?:/[\w-./?%&=]*)?$"
        return bool(re.match(pattern, url))

    @staticmethod
    def sanitize_html(html: str, allowed_tags: Optional[List[str]] = None) -> str:
        """
        Sanitize HTML content.

        Args:
            html: HTML content to sanitize
            allowed_tags: List of allowed HTML tags

        Returns:
            str: Sanitized HTML
        """
        default_allowed = [
            "p",
            "br",
            "strong",
            "em",
            "u",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
            "a",
            "img",
            "blockquote",
            "code",
            "pre",
        ]
        tags = allowed_tags or default_allowed
        return bleach.clean(html, tags=tags, strip=True)

    @staticmethod
    def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
        """
        Validate date range.

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            bool: True if valid
        """
        return start_date <= end_date

    @classmethod
    def validate_required_fields(
        cls, data: Dict, required_fields: List[str]
    ) -> List[str]:
        """
        Validate required fields in data.

        Args:
            data: Data dictionary to validate
            required_fields: List of required field names

        Returns:
            List[str]: List of missing field names
        """
        missing = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                missing.append(field)
        return missing


# ==============================
# Response Formatting Helpers
# ==============================


class ResponseFormatter:
    """Utility class for formatting API responses."""

    @staticmethod
    def format_data_response(
        data: Any, message: Optional[str] = None, metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Format successful data response.

        Args:
            data: Response data
            message: Optional message
            metadata: Optional metadata

        Returns:
            Dict: Formatted response
        """
        response = {"status": "success", "data": data}

        if message:
            response["message"] = message
        if metadata:
            response["metadata"] = metadata

        return response

    @staticmethod
    def format_error_response(
        message: str,
        errors: Optional[Union[str, List, Dict]] = None,
        code: Optional[str] = None,
    ) -> Dict:
        """
        Format error response.

        Args:
            message: Error message
            errors: Detailed errors
            code: Error code

        Returns:
            Dict: Formatted error response
        """
        response = {"status": "error", "message": message}

        if errors:
            response["errors"] = errors
        if code:
            response["code"] = code

        return response

    @staticmethod
    def format_pagination_data(
        data: List, total: int, page: int, per_page: int
    ) -> Dict:
        """
        Format paginated response.

        Args:
            data: Page data
            total: Total number of items
            page: Current page number
            per_page: Items per page

        Returns:
            Dict: Formatted pagination data
        """
        total_pages = (total + per_page - 1) // per_page

        return {
            "data": data,
            "pagination": {
                "total": total,
                "per_page": per_page,
                "current_page": page,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
        }

    @staticmethod
    def format_serializer_errors(errors: Dict) -> Dict:
        """
        Format serializer validation errors.

        Args:
            errors: Serializer errors dictionary

        Returns:
            Dict: Formatted errors
        """
        formatted_errors = {}

        for field, error_list in errors.items():
            if isinstance(error_list, dict):
                formatted_errors[field] = ResponseFormatter.format_serializer_errors(
                    error_list
                )
            else:
                formatted_errors[field] = (
                    error_list[0] if isinstance(error_list, list) else error_list
                )

        return formatted_errors


def sanitize_svg(svg_content):
    """
    Sanitize SVG content to prevent XSS attacks.
    """
    # List of allowed SVG tags
    ALLOWED_TAGS = {
        "svg",
        "path",
        "circle",
        "rect",
        "line",
        "polyline",
        "polygon",
        "text",
        "g",
        "defs",
        "title",
        "desc",
        "style",
    }

    # List of allowed attributes
    ALLOWED_ATTRIBUTES = {
        "viewbox",
        "width",
        "height",
        "xmlns",
        "version",
        "baseprofile",
        "x",
        "y",
        "x1",
        "y1",
        "x2",
        "y2",
        "r",
        "d",
        "transform",
        "style",
        "fill",
        "stroke",
        "stroke-width",
        "class",
        "id",
    }

    try:
        tree = ElementTree.fromstring(svg_content)

        # Check for potentially malicious content
        for elem in tree.iter():
            # Remove script elements and event handlers
            if elem.tag.lower() == "script" or any(
                attr.lower().startswith("on") for attr in elem.attrib.keys()
            ):
                raise ValidationError("SVG contains potentially malicious content")

            # Remove any non-allowed tags
            if elem.tag.split("}")[-1].lower() not in ALLOWED_TAGS:
                raise ValidationError(f"SVG contains non-allowed tag: {elem.tag}")

            # Remove any non-allowed attributes
            allowed_attrs = elem.attrib.copy()
            for attr in elem.attrib:
                if attr.split("}")[-1].lower() not in ALLOWED_ATTRIBUTES:
                    del allowed_attrs[attr]
            elem.attrib = allowed_attrs

        # Check for potentially malicious content in style attributes
        for elem in tree.iter():
            style = elem.get("style", "")
            if style and ("javascript:" in style or "expression(" in style):
                raise ValidationError(
                    "SVG contains potentially malicious style content"
                )

        return ElementTree.tostring(tree, encoding="unicode")

    except ElementTree.ParseError:
        raise ValidationError("Invalid SVG content")


def validate_svg_file(file):
    """
    Validate and sanitize an uploaded SVG file.
    """
    try:
        content = file.read().decode("utf-8")
        sanitized_content = sanitize_svg(content)
        return sanitized_content
    except (UnicodeDecodeError, ValidationError) as e:
        raise ValidationError(f"Invalid SVG file: {str(e)}")
    finally:
        file.seek(0)  # Reset file pointer
