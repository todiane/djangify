from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service class for handling email operations
    """

    @staticmethod
    def send_verification_email(user, request):
        """
        Send email verification link to user
        """
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}"

            context = {
                "user": user,
                "verification_url": verification_url,
                "site_name": settings.SITE_NAME,
            }

            html_message = render_to_string("emails/verify_email.html", context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject="Verify your email address",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending verification email: {str(e)}")
            return False

    @staticmethod
    def send_password_reset_email(user, request):
        """
        Send password reset link to user
        """
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

            context = {
                "user": user,
                "reset_url": reset_url,
                "site_name": settings.SITE_NAME,
            }

            html_message = render_to_string("emails/reset_password.html", context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject="Reset your password",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending password reset email: {str(e)}")
            return False
