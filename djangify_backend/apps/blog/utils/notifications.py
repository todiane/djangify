from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.conf import settings
from djangify_backend.apps.blog.models import Comment


class NotificationManager:
    """
    Handles notifications for the blog system
    """

    @staticmethod
    def send_comment_notification(comment: "Comment") -> None:
        """
        Send notification when a new comment is posted
        """
        # Email to admin
        subject = f"New comment on: {comment.post.title}"
        html_message = render_to_string(
            "blog/email/new_comment.html",
            {
                "comment": comment,
                "post": comment.post,
                "admin_url": f"/admin/blog/comment/{comment.id}/change/",
            },
        )

        send_mail(
            subject=subject,
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
        )

    @staticmethod
    def send_comment_approval_notification(comment: "Comment") -> None:
        """
        Send notification when a comment is approved
        """
        subject = "Your comment has been approved"
        html_message = render_to_string(
            "blog/email/comment_approved.html",
            {"comment": comment, "post": comment.post},
        )

        send_mail(
            subject=subject,
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.email],
            html_message=html_message,
        )

    @staticmethod
    def send_comment_rejection_notification(
        comment: "Comment", reason: str = None
    ) -> None:
        """
        Send notification when a comment is rejected
        """
        subject = "Regarding your comment"
        html_message = render_to_string(
            "blog/email/comment_rejected.html",
            {"comment": comment, "post": comment.post, "reason": reason},
        )

        send_mail(
            subject=subject,
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.email],
            html_message=html_message,
        )
