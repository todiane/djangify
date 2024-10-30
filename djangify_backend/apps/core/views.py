from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet class with common functionality
    """

    def get_response_data(
        self,
        data: Any = None,
        message: str = None,
        status: str = "success",
        extra: Dict = None,
    ) -> Dict:
        """Create standardized response format"""
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
        """Create a success response"""
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
        """Create an error response"""
        return Response(
            self.get_response_data(data, message, "error", extra), status=status_code
        )

    def handle_exception(self, exc):
        """Global exception handler for viewset"""
        logger.error(f"Error in {self.__class__.__name__}: {str(exc)}")
        return self.error_response(
            message=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
