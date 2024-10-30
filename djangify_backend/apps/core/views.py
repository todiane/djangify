from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.core.cache import cache
from typing import Any, Dict
import logging
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .emails import EmailService

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


User = get_user_model()


@api_view(["POST"])
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"detail": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST
        )
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {"detail": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def request_password_reset(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
        EmailService.send_password_reset_email(user, request)
        return Response(
            {"detail": "Password reset email sent"}, status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {"detail": "User with this email does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )
