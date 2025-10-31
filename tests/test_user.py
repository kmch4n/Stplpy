"""
Tests for User class.
"""
import pytest
from unittest.mock import Mock, patch, mock_open
from stplpy.user import User
from stplpy.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    APIError
)


class TestUserInit:
    """Tests for User initialization."""

    def test_user_init(self, mock_token):
        """Test User class initialization."""
        user = User(mock_token)
        assert user.token == mock_token
        assert "Authorization" in user.headers
        assert user.headers["Authorization"] == f"OAuth {mock_token}"
        assert "User-Agent" in user.headers


class TestGetMyself:
    """Tests for get_myself method."""

    @patch('stplpy.user.requests.get')
    def test_get_myself_success(self, mock_get, mock_token, mock_user_data):
        """Test successful get_myself call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_user_data
        mock_get.return_value = mock_response

        user = User(mock_token)
        result = user.get_myself()

        assert result == mock_user_data
        mock_get.assert_called_once()

    @patch('stplpy.user.requests.get')
    def test_get_myself_authentication_error(self, mock_get, mock_token):
        """Test get_myself with authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        user = User(mock_token)
        with pytest.raises(AuthenticationError):
            user.get_myself()

    @patch('stplpy.user.requests.get')
    def test_get_myself_api_error(self, mock_get, mock_token):
        """Test get_myself with API error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        user = User(mock_token)
        with pytest.raises(APIError) as exc_info:
            user.get_myself()
        assert exc_info.value.status_code == 500


class TestGetUser:
    """Tests for get_user method."""

    @patch('stplpy.user.requests.get')
    def test_get_user_success(self, mock_get, mock_token, mock_user_data):
        """Test successful get_user call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_user_data
        mock_get.return_value = mock_response

        user = User(mock_token)
        result = user.get_user("test_user")

        assert result == mock_user_data
        assert "test_user" in mock_get.call_args[0][0]

    @patch('stplpy.user.requests.get')
    def test_get_user_not_found(self, mock_get, mock_token):
        """Test get_user with user not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        user = User(mock_token)
        with pytest.raises(ResourceNotFoundError):
            user.get_user("nonexistent_user")


class TestFollowUser:
    """Tests for follow_user method."""

    @patch('stplpy.user.requests.post')
    def test_follow_user_success(self, mock_post, mock_token):
        """Test successful follow_user call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        user = User(mock_token)
        result = user.follow_user("target_user")

        assert result is True
        mock_post.assert_called_once()

    @patch('stplpy.user.requests.post')
    def test_follow_user_not_found(self, mock_post, mock_token):
        """Test follow_user with user not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        user = User(mock_token)
        with pytest.raises(ResourceNotFoundError):
            user.follow_user("nonexistent_user")


class TestUpdateProfilePicture:
    """Tests for update_profile_picture method."""

    @patch('stplpy.user.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b'image_data')
    def test_update_profile_picture_success(self, mock_file, mock_post, mock_token):
        """Test successful profile picture update."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response

        user = User(mock_token)
        result = user.update_profile_picture("/path/to/image.jpg")

        assert result is True
        mock_post.assert_called_once()

    def test_update_profile_picture_file_not_found(self, mock_token):
        """Test update_profile_picture with file not found."""
        user = User(mock_token)
        with pytest.raises(ValidationError):
            user.update_profile_picture("/nonexistent/file.jpg")
