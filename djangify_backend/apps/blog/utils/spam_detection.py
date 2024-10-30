import re
import requests
from typing import Tuple


class SpamDetector:
    """
    Spam detection utility for blog comments
    """

    def __init__(self):
        self.blacklist_words = {
            "viagra",
            "cialis",
            "poker",
            "casino",
            "loan",
            "payday",
            "mortgage",
            "free money",
        }

    def check_comment(self, content: str, email: str, name: str) -> Tuple[bool, str]:
        """
        Check if a comment is spam
        Returns: (is_spam: bool, reason: str)
        """
        # Check for blacklisted words
        content_lower = content.lower()
        for word in self.blacklist_words:
            if word in content_lower:
                return True, f"Blacklisted word detected: {word}"

        # Check for excessive URLs
        urls = re.findall(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            content,
        )
        if len(urls) > 2:
            return True, "Too many URLs in comment"

        # Check for repetitive characters
        if re.search(r"(.)\1{4,}", content):
            return True, "Repetitive characters detected"

        # Check for all caps
        words = content.split()
        caps_words = sum(1 for word in words if word.isupper() and len(word) > 2)
        if caps_words / len(words) > 0.5:
            return True, "Too many capitalized words"

        # Check if email is from disposable email provider
        email_domain = email.split("@")[1].lower()
        disposable_domains = {"tempmail.com", "throwawaymail.com"}
        if email_domain in disposable_domains:
            return True, "Disposable email address detected"

        return False, ""

    async def check_ip_reputation(self, ip_address: str) -> Tuple[bool, str]:
        """
        Check IP reputation using external API
        Note: Implement with your preferred IP reputation service
        """
        try:
            # Example using a hypothetical API service
            # response = requests.get(f"https://api.ipreputation.net/check/{ip_address}")
            # return response.json()['is_suspicious'], response.json()['reason']
            return False, ""
        except Exception as e:
            return False, f"IP reputation check failed: {str(e)}"
