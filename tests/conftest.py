"""
Pytest configuration and fixtures for Stplpy tests.
"""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_token():
    """Provide a mock OAuth token for testing."""
    return "test_oauth_token_1234567890"


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"test": "data"}
    return mock


@pytest.fixture
def mock_user_data():
    """Provide sample user data."""
    return {
        "user_id": "12345",
        "username": "test_user",
        "user_image_url": "https://example.com/image.jpg",
        "user_relationship_id": "rel_123"
    }


@pytest.fixture
def mock_timeline_data():
    """Provide sample timeline data."""
    return {
        "feeds": [
            {
                "post_id": "post_1",
                "user_id": "12345",
                "comment": "Test study record",
                "duration": 3600
            }
        ],
        "next": "next_cursor_token"
    }
