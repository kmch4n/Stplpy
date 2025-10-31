"""
Custom exceptions for Stplpy library.
"""


class StudyPlusError(Exception):
    """Base exception for all StudyPlus related errors."""
    pass


class AuthenticationError(StudyPlusError):
    """Raised when authentication fails."""
    pass


class RateLimitError(StudyPlusError):
    """Raised when API rate limit is exceeded."""
    pass


class ResourceNotFoundError(StudyPlusError):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(StudyPlusError):
    """Raised when input validation fails."""
    pass


class APIError(StudyPlusError):
    """Raised when API returns an error response."""

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
