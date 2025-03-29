"""
Tests for the authentication module.
"""

import json
import logging
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI, Request
from starlette.testclient import TestClient

from reten_service_core.auth.api_key import APIKeyAuth, get_api_key
from reten_service_core.core.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def setup_environment():
    """Set up environment variables required for tests."""
    os.environ["VALID_API_KEYS"] = json.dumps(["test-key"])
    os.environ["GCP_PROJECT_ID"] = "test-project"
    yield
    if "VALID_API_KEYS" in os.environ:
        del os.environ["VALID_API_KEYS"]
    if "GCP_PROJECT_ID" in os.environ:
        del os.environ["GCP_PROJECT_ID"]


@pytest.fixture
def test_settings():
    """Test settings fixture."""
    with patch("reten_service_core.auth.api_key.get_settings") as mock:
        mock.return_value = Settings(
            VALID_API_KEYS=["test-key-1", "test-key-2"],
            GCP_PROJECT_ID="test-project",
            LOG_FORMAT="json",
            LOG_LEVEL="INFO",
        )
        yield mock.return_value


@pytest.fixture
def app():
    """Create a test FastAPI application."""
    app = FastAPI()

    @app.get("/protected")
    async def protected_route(request: Request):
        api_key = get_api_key(request)
        return {"message": "success", "key": api_key}

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


@pytest.fixture
def client(app, test_settings):
    """Create a test client."""
    app.add_middleware(
        APIKeyAuth,
        exclude_paths=["/health"],
        log_invalid_attempts=True,
    )
    return TestClient(app)


def test_api_key_auth_initialization():
    """Test APIKeyAuth initialization with custom parameters."""
    auth = APIKeyAuth(app=FastAPI(), header_name="Custom-API-Key", exclude_paths=["/public"])
    assert auth.header_name == "Custom-API-Key"
    assert auth.exclude_paths == ["/public"]


def test_api_key_auth_default_initialization():
    """Test APIKeyAuth initialization with default parameters."""
    auth = APIKeyAuth(app=FastAPI())
    assert auth.header_name == "X-API-Key"
    assert auth.exclude_paths == ["/docs", "/redoc", "/openapi.json"]


def test_api_key_auth_valid_key(app, client):
    """Test APIKeyAuth with valid API key."""
    app.add_middleware(APIKeyAuth)
    response = client.get("/protected", headers={"X-API-Key": "test-key-1"})
    assert response.status_code == 200
    assert response.json() == {"message": "success", "key": "test-key-1"}


def test_api_key_auth_invalid_key(app, client):
    """Test APIKeyAuth with invalid API key."""
    app.add_middleware(APIKeyAuth)
    response = client.get("/protected", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "invalid_api_key",
        "detail": "Invalid API key",
        "type": "authentication_error",
    }


def test_api_key_auth_missing_key(app, client):
    """Test APIKeyAuth with missing API key."""
    app.add_middleware(APIKeyAuth)
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json() == {
        "error": "missing_api_key",
        "detail": "No API key provided in X-API-Key header",
        "type": "authentication_error",
    }


def test_api_key_auth_excluded_path(app):
    """Test APIKeyAuth with excluded path."""
    app.add_middleware(APIKeyAuth, exclude_paths=["/health"])
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_key_auth_custom_header(app):
    """Test APIKeyAuth with custom header name."""
    app.add_middleware(APIKeyAuth, header_name="Custom-API-Key")
    client = TestClient(app)
    response = client.get("/protected", headers={"Custom-API-Key": "test-key"})
    assert response.status_code == 200
    assert response.json() == {"message": "success", "key": "test-key"}


def test_api_key_auth_invalid_custom_header(app, client):
    """Test APIKeyAuth with invalid custom header name."""
    app.add_middleware(APIKeyAuth, header_name="Custom-API-Key")
    response = client.get(
        "/protected",
        headers={"X-API-Key": "test-key-1"},  # Using default header name
    )
    assert response.status_code == 401
    assert response.json() == {
        "error": "missing_api_key",
        "detail": "No API key provided in Custom-API-Key header",
        "type": "authentication_error",
    }


def test_valid_api_key(client):
    """Test request with valid API key."""
    response = client.get(
        "/protected",
        headers={"X-API-Key": "test-key-1"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "success",
        "key": "test-key-1",
    }


def test_invalid_api_key(client, caplog):
    """Test request with invalid API key."""
    with caplog.at_level(logging.WARNING):
        response = client.get(
            "/protected",
            headers={"X-API-Key": "invalid-key"},
        )

    assert response.status_code == 401
    assert response.json() == {
        "error": "invalid_api_key",
        "detail": "Invalid API key",
        "type": "authentication_error",
    }

    # Check that the attempt was logged
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "WARNING"
    assert record.message == "Authentication failed"
    assert "error_type" in record.__dict__
    assert record.__dict__["error_type"] == "invalid_api_key"


def test_missing_api_key(client, caplog):
    """Test request without API key."""
    with caplog.at_level(logging.WARNING):
        response = client.get("/protected")

    assert response.status_code == 401
    assert response.json() == {
        "error": "missing_api_key",
        "detail": "No API key provided in X-API-Key header",
        "type": "authentication_error",
    }

    # Check that the attempt was logged
    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Authentication failed"
    assert caplog.records[0].__dict__["error_type"] == "missing_api_key"


def test_excluded_path(client):
    """Test request to excluded path."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_custom_header_name(app, test_settings):
    """Test middleware with custom header name."""
    app.add_middleware(APIKeyAuth, header_name="X-Custom-Key")
    client = TestClient(app)

    response = client.get(
        "/protected",
        headers={"X-Custom-Key": "test-key-1"},
    )
    assert response.status_code == 200


def test_multiple_api_keys(client):
    """Test multiple valid API keys."""
    # Test first key
    response = client.get(
        "/protected",
        headers={"X-API-Key": "test-key-1"},
    )
    assert response.status_code == 200

    # Test second key
    response = client.get(
        "/protected",
        headers={"X-API-Key": "test-key-2"},
    )
    assert response.status_code == 200


def test_path_exclusion_patterns(app, test_settings):
    """Test path exclusion patterns."""
    app.add_middleware(
        APIKeyAuth,
        exclude_paths=["/public", "/health/"],
    )
    client = TestClient(app)

    # Test exact match
    response = client.get("/public")
    assert response.status_code == 404  # Not found, but not auth error

    # Test prefix match
    response = client.get("/health/check")
    assert response.status_code == 404  # Not found, but not auth error

    # Test non-excluded path
    response = client.get("/protected")
    assert response.status_code == 401  # Auth error
    assert response.json()["error"] == "missing_api_key"


def test_get_api_key_helper(app, test_settings):
    """Test get_api_key helper function."""
    app.add_middleware(APIKeyAuth)
    client = TestClient(app)

    # Test with valid key
    response = client.get(
        "/protected",
        headers={"X-API-Key": "test-key-1"},
    )
    assert response.status_code == 200
    assert response.json()["key"] == "test-key-1"


def test_logging_disabled(app, test_settings, caplog):
    """Test middleware with logging disabled."""
    app.add_middleware(APIKeyAuth, log_invalid_attempts=False)
    client = TestClient(app)

    with caplog.at_level(logging.WARNING):
        response = client.get(
            "/protected",
            headers={"X-API-Key": "invalid-key"},
        )

    assert response.status_code == 401
    assert len(caplog.records) == 0  # No log records


def test_get_settings(tmp_path):
    """Test get_settings function."""
    import json
    import os
    from pathlib import Path

    # Clear the LRU cache
    get_settings.cache_clear()

    # Create a temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text(
        f"VALID_API_KEYS={json.dumps(['test-key-1', 'test-key-2'])}\nGCP_PROJECT_ID=test-project\n"
    )

    # Set environment variables
    os.environ["VALID_API_KEYS"] = json.dumps(["test-key-1", "test-key-2"])
    os.environ["GCP_PROJECT_ID"] = "test-project"

    # Create a symlink to the .env file in the current directory
    current_env = Path(".env")
    if current_env.exists():
        current_env.unlink()
    current_env.symlink_to(env_file)

    try:
        # First call should create settings
        settings1 = get_settings()
        assert settings1.log_level == "INFO"
        assert settings1.log_format == "json"
        assert settings1.valid_api_keys == ["test-key-1", "test-key-2"]
        assert settings1.gcp_project_id == "test-project"

        # Second call should return cached instance
        settings2 = get_settings()
        assert settings1 is settings2  # Same instance due to @lru_cache
    finally:
        # Clean up
        current_env.unlink()
        del os.environ["VALID_API_KEYS"]
        del os.environ["GCP_PROJECT_ID"]
        get_settings.cache_clear()  # Clear cache for other tests


def test_settings_parse_env_var():
    """Test parse_env_var method."""
    from reten_service_core.core.settings import Settings

    # Test JSON parsing
    assert Settings.parse_env_var("valid_api_keys", '["key1", "key2"]') == ["key1", "key2"]

    # Test comma-separated parsing
    assert Settings.parse_env_var("valid_api_keys", "key1,key2") == ["key1", "key2"]

    # Test other fields
    assert Settings.parse_env_var("log_level", "DEBUG") == "DEBUG"


def test_settings_defaults():
    """Test settings default values."""
    import json
    import os

    # Clear the LRU cache
    get_settings.cache_clear()

    # Set required environment variables
    os.environ["VALID_API_KEYS"] = json.dumps(["test-key"])
    os.environ["GCP_PROJECT_ID"] = "test-project"

    try:
        settings = get_settings()
        assert settings.log_level == "INFO"
        assert settings.log_format == "json"
        assert settings.gcp_service_account_path is None
        assert settings.project_name == "Reten Service"
        assert settings.version == "0.1.0"
        assert settings.description == "Reten Service Core"
    finally:
        # Clean up
        del os.environ["VALID_API_KEYS"]
        del os.environ["GCP_PROJECT_ID"]
        get_settings.cache_clear()


def test_api_key_rate_limit_error():
    """Test APIKeyRateLimitError exception."""
    from reten_service_core.auth.exceptions import APIKeyRateLimitError

    # Test with default values
    error = APIKeyRateLimitError()
    assert error.status_code == 429
    assert error.detail == "API key rate limit exceeded"
    assert error.error_type == "rate_limit_exceeded"
    assert error.extra == {}

    # Test with custom values
    custom_headers = {"Retry-After": "60"}
    custom_extra = {"limit": 100, "current": 150}
    error = APIKeyRateLimitError(
        detail="Rate limit of 100 requests per minute exceeded",
        headers=custom_headers,
        extra=custom_extra,
    )
    assert error.status_code == 429
    assert error.detail == "Rate limit of 100 requests per minute exceeded"
    assert error.error_type == "rate_limit_exceeded"
    assert error.headers == custom_headers
    assert error.extra == custom_extra


def test_api_key_permission_error():
    """Test APIKeyPermissionError exception."""
    from reten_service_core.auth.exceptions import APIKeyPermissionError

    # Test with default values
    error = APIKeyPermissionError()
    assert error.status_code == 403
    assert error.detail == "API key lacks required permissions"
    assert error.error_type == "insufficient_permissions"
    assert error.extra == {}

    # Test with custom values
    custom_headers = {"X-Required-Permission": "admin"}
    custom_extra = {"required": "admin", "current": "user"}
    error = APIKeyPermissionError(
        detail="Admin permission required",
        headers=custom_headers,
        extra=custom_extra,
    )
    assert error.status_code == 403
    assert error.detail == "Admin permission required"
    assert error.error_type == "insufficient_permissions"
    assert error.headers == custom_headers
    assert error.extra == custom_extra
