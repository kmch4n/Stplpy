"""
Tests for Timeline class.
"""
import pytest
from unittest.mock import Mock, patch
from stplpy.timeline import Timeline
from stplpy.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitError,
    APIError
)
from requests.exceptions import HTTPError


class TestTimelineInit:
    """Tests for Timeline initialization."""

    def test_timeline_init(self, mock_token):
        """Test Timeline class initialization."""
        timeline = Timeline(mock_token)
        assert timeline.token == mock_token
        assert "Authorization" in timeline.headers
        assert timeline.headers["Authorization"] == f"OAuth {mock_token}"


class TestCreateToken:
    """Tests for create_token method."""

    def test_create_token_default_length(self, mock_token):
        """Test create_token with default length."""
        timeline = Timeline(mock_token)
        token = timeline.create_token()
        assert len(token) == 10
        assert token.isalnum()

    def test_create_token_custom_length(self, mock_token):
        """Test create_token with custom length."""
        timeline = Timeline(mock_token)
        token = timeline.create_token(20)
        assert len(token) == 20
        assert token.isalnum()


class TestLikePost:
    """Tests for like_post method."""

    @patch('stplpy.timeline.requests.post')
    def test_like_post_success(self, mock_post, mock_token):
        """Test successful like_post call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        timeline = Timeline(mock_token)
        result = timeline.like_post("post_123")

        assert result is True
        mock_post.assert_called_once()

    @patch('stplpy.timeline.requests.post')
    def test_like_post_not_found(self, mock_post, mock_token):
        """Test like_post with post not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status = Mock(side_effect=HTTPError())
        mock_post.return_value = mock_response

        timeline = Timeline(mock_token)
        with pytest.raises(ResourceNotFoundError):
            timeline.like_post("nonexistent_post")

    @patch('stplpy.timeline.requests.post')
    def test_like_post_rate_limit(self, mock_post, mock_token):
        """Test like_post with rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status = Mock(side_effect=HTTPError())
        mock_post.return_value = mock_response

        timeline = Timeline(mock_token)
        with pytest.raises(RateLimitError):
            timeline.like_post("post_123")


class TestSendComment:
    """Tests for send_comment method."""

    @patch('stplpy.timeline.requests.post')
    def test_send_comment_success(self, mock_post, mock_token):
        """Test successful send_comment call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"comment_id": "comment_123"}
        mock_post.return_value = mock_response

        timeline = Timeline(mock_token)
        result = timeline.send_comment("post_123", "Great work!")

        assert result == {"comment_id": "comment_123"}
        mock_post.assert_called_once()


class TestPostStudyRecord:
    """Tests for post_study_record method."""

    @patch('stplpy.timeline.requests.post')
    def test_post_study_record_success(self, mock_post, mock_token):
        """Test successful post_study_record call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"record_id": "record_123"}
        mock_post.return_value = mock_response

        timeline = Timeline(mock_token)
        result = timeline.post_study_record(
            material_code="mat_123",
            duration=3600,
            comment="Studied hard today"
        )

        assert result == {"record_id": "record_123"}
        mock_post.assert_called_once()


class TestGetFolloweeTimeline:
    """Tests for get_followee_timeline method."""

    @patch('stplpy.timeline.requests.get')
    def test_get_followee_timeline_success(self, mock_get, mock_token, mock_timeline_data):
        """Test successful get_followee_timeline call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = mock_timeline_data
        mock_get.return_value = mock_response

        timeline = Timeline(mock_token)
        result = timeline.get_followee_timeline()

        assert result == mock_timeline_data
        mock_get.assert_called_once()

    @patch('stplpy.timeline.requests.get')
    def test_get_followee_timeline_with_until(self, mock_get, mock_token, mock_timeline_data):
        """Test get_followee_timeline with until parameter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = mock_timeline_data
        mock_get.return_value = mock_response

        timeline = Timeline(mock_token)
        result = timeline.get_followee_timeline(until="cursor_123")

        assert result == mock_timeline_data
        assert "until=cursor_123" in mock_get.call_args[0][0]


class TestHandleHttpError:
    """Tests for _handle_http_error method."""

    def test_handle_http_error_404(self, mock_token):
        """Test _handle_http_error with 404 status."""
        timeline = Timeline(mock_token)
        mock_response = Mock()
        mock_response.status_code = 404
        http_err = HTTPError()

        with pytest.raises(ResourceNotFoundError):
            timeline._handle_http_error(mock_response, "Test message", http_err)

    def test_handle_http_error_401(self, mock_token):
        """Test _handle_http_error with 401 status."""
        timeline = Timeline(mock_token)
        mock_response = Mock()
        mock_response.status_code = 401
        http_err = HTTPError()

        with pytest.raises(AuthenticationError):
            timeline._handle_http_error(mock_response, "Test message", http_err)

    def test_handle_http_error_429(self, mock_token):
        """Test _handle_http_error with 429 status."""
        timeline = Timeline(mock_token)
        mock_response = Mock()
        mock_response.status_code = 429
        http_err = HTTPError()

        with pytest.raises(RateLimitError):
            timeline._handle_http_error(mock_response, "Test message", http_err)

    def test_handle_http_error_500(self, mock_token):
        """Test _handle_http_error with 500 status."""
        timeline = Timeline(mock_token)
        mock_response = Mock()
        mock_response.status_code = 500
        http_err = HTTPError()

        with pytest.raises(APIError) as exc_info:
            timeline._handle_http_error(mock_response, "Test message", http_err)
        assert exc_info.value.status_code == 500
