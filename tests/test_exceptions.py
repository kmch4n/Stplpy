"""
Tests for custom exception classes.
"""
import pytest
from stplpy.exceptions import (
    StudyPlusError,
    APIError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError
)


def test_study_plus_error_base():
    """Test that StudyPlusError is the base exception."""
    error = StudyPlusError("Base error")
    assert isinstance(error, Exception)
    assert str(error) == "Base error"


def test_api_error():
    """Test APIError with status code."""
    error = APIError("API failed", status_code=500)
    assert isinstance(error, StudyPlusError)
    assert str(error) == "API failed"
    assert error.status_code == 500


def test_api_error_without_status_code():
    """Test APIError without status code."""
    error = APIError("API failed")
    assert error.status_code is None


def test_authentication_error():
    """Test AuthenticationError."""
    error = AuthenticationError("Auth failed")
    assert isinstance(error, StudyPlusError)
    assert str(error) == "Auth failed"


def test_resource_not_found_error():
    """Test ResourceNotFoundError."""
    error = ResourceNotFoundError("Resource not found")
    assert isinstance(error, StudyPlusError)
    assert str(error) == "Resource not found"


def test_validation_error():
    """Test ValidationError."""
    error = ValidationError("Validation failed")
    assert isinstance(error, StudyPlusError)
    assert str(error) == "Validation failed"


def test_rate_limit_error():
    """Test RateLimitError."""
    error = RateLimitError("Rate limit exceeded")
    assert isinstance(error, StudyPlusError)
    assert str(error) == "Rate limit exceeded"


def test_exception_inheritance_chain():
    """Test that all custom exceptions inherit from StudyPlusError."""
    exceptions = [
        APIError("test"),
        AuthenticationError("test"),
        ResourceNotFoundError("test"),
        ValidationError("test"),
        RateLimitError("test")
    ]

    for exc in exceptions:
        assert isinstance(exc, StudyPlusError)
        assert isinstance(exc, Exception)
