from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.translation import gettext_lazy as _
from typing import Optional, Any, Dict
import logging

logger = logging.getLogger(__name__)


class CacheMixin:
    """
    Mixin to add caching support to ViewSets.
    Provides configurable cache timeouts and key generation.
    """

    cache_timeout: int = getattr(
        settings, "DEFAULT_CACHE_TIMEOUT", 300
    )  # 5 minutes default
    cache_key_prefix: str = ""

    def get_cache_key(self, view_name: str, **kwargs) -> str:
        """Generate a unique cache key for the request."""
        key_parts = [self.cache_key_prefix, self.basename, view_name]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return ":".join(filter(None, key_parts))

    def cache_response(
        self, key: str, data: Any, timeout: Optional[int] = None
    ) -> None:
        """Cache the response data with the specified key."""
        cache.set(key, data, timeout or self.cache_timeout)

    def get_cached_response(self, key: str) -> Optional[Any]:
        """Retrieve cached response data."""
        return cache.get(key)


class ResponseMixin:
    """
    Mixin to provide standardized response formats.
    Ensures consistent API response structure.
    """

    def get_response_data(
        self,
        data: Any = None,
        message: str = None,
        status: str = "success",
        extra: Dict = None,
    ) -> Dict:
        """
        Create a standardized response dictionary.

        Args:
            data: The main response data
            message: Optional message to include
            status: Response status indicator ('success' or 'error')
            extra: Additional data to include in response
        """
        response = {
            "status": status,
            "data": data,
        }
        if message:
            response["message"] = message
        if extra:
            response.update(extra)
        return response

    def success_response(
        self,
        data: Any = None,
        message: str = None,
        status_code: int = status.HTTP_200_OK,
        **extra,
    ) -> Response:
        """Create a success response."""
        return Response(
            self.get_response_data(data, message, "success", extra), status=status_code
        )

    def error_response(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Any = None,
        **extra,
    ) -> Response:
        """Create an error response."""
        return Response(
            self.get_response_data(data, message, "error", extra), status=status_code
        )


class BaseViewSet(CacheMixin, ResponseMixin, viewsets.ModelViewSet):
    """
    Base ViewSet combining caching and response formatting with standard CRUD operations.
    Implements common functionality for all ViewSets in the application.
    """

    @method_decorator(cache_page(300))  # Cache list view for 5 minutes
    def list(self, request, *args, **kwargs):
        """List objects with caching and standard response format."""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data, message=_("Objects retrieved successfully")
            )
        except Exception as e:
            logger.error(f"Error in list view: {str(e)}")
            return self.error_response(
                message=_("Failed to retrieve objects"),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single object with caching."""
        cache_key = self.get_cache_key("retrieve", pk=kwargs.get("pk"))
        cached_data = self.get_cached_response(cache_key)

        if cached_data:
            return self.success_response(
                data=cached_data, message=_("Object retrieved from cache")
            )

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            self.cache_response(cache_key, serializer.data)

            return self.success_response(
                data=serializer.data, message=_("Object retrieved successfully")
            )
        except Exception as e:
            logger.error(f"Error in retrieve view: {str(e)}")
            return self.error_response(
                message=_("Failed to retrieve object"),
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request, *args, **kwargs):
        """Create a new object."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return self.success_response(
                data=serializer.data,
                message=_("Object created successfully"),
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Error in create view: {str(e)}")
            return self.error_response(
                message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """Update an existing object."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=kwargs.get("partial", False)
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Invalidate cache
            cache_key = self.get_cache_key("retrieve", pk=instance.pk)
            cache.delete(cache_key)

            return self.success_response(
                data=serializer.data, message=_("Object updated successfully")
            )
        except Exception as e:
            logger.error(f"Error in update view: {str(e)}")
            return self.error_response(
                message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """Delete an object."""
        try:
            instance = self.get_object()
            # Invalidate cache before deletion
            cache_key = self.get_cache_key("retrieve", pk=instance.pk)
            cache.delete(cache_key)

            self.perform_destroy(instance)
            return self.success_response(
                message=_("Object deleted successfully"),
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error(f"Error in destroy view: {str(e)}")
            return self.error_response(
                message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        """Bulk create objects."""
        try:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)

            return self.success_response(
                data=serializer.data,
                message=_("Objects created successfully"),
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Error in bulk create: {str(e)}")
            return self.error_response(
                message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )

    def perform_bulk_create(self, serializer):
        """Perform bulk creation of objects."""
        serializer.save()
