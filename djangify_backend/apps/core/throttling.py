from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class BurstRateThrottle(AnonRateThrottle):
    """
    Throttle for burst requests - stricter limit for short time period
    """

    scope = "burst"
    rate = "10/minute"  # Adjust as needed


class SustainedRateThrottle(AnonRateThrottle):
    """
    Throttle for sustained requests - more lenient limit over longer period
    """

    scope = "sustained"
    rate = "100/hour"  # Adjust as needed


class UserBurstRateThrottle(UserRateThrottle):
    """
    Throttle for authenticated user burst requests
    """

    scope = "user_burst"
    rate = "20/minute"  # Adjust as needed


class UserSustainedRateThrottle(UserRateThrottle):
    """
    Throttle for authenticated user sustained requests
    """

    scope = "user_sustained"
    rate = "200/hour"  # Adjust as needed


class APIEndpointThrottle(UserRateThrottle):
    """
    Base throttle class for specific API endpoints
    Subclass this for different endpoints with different rates
    """

    def parse_rate(self, rate):
        """
        Override to allow dynamic rate setting
        """
        if not getattr(self, "rate", None):
            self.rate = rate
        return super().parse_rate(self.rate)


class WriteOperationThrottle(APIEndpointThrottle):
    """
    Specific throttle for write operations (POST, PUT, PATCH, DELETE)
    """

    scope = "write_operations"
    rate = "30/hour"  # Adjust as needed

    def allow_request(self, request, view):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return super().allow_request(request, view)
        return True
