"""
Authentication exceptions module.

This module defines custom exceptions for authentication-related errors.
"""

from typing import Any

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_429_TOO_MANY_REQUESTS


class AuthError(HTTPException):
    """Base class for authentication errors."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_type: str,
        headers: dict[str, str] | None = None,
        extra: dict[str, Any] | None = None,
    ):
        """
        Initialize the authentication error.

        Args:
            status_code: HTTP status code
            detail: Error description
            error_type: Type of error for categorization
            headers: Optional response headers
            extra: Optional additional error context
        """
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_type = error_type
        self.extra = extra or {}


class InvalidAPIKeyError(AuthError):
    """Error raised when an invalid API key is provided."""

    def __init__(
        self,
        detail: str = "Invalid API key provided",
        headers: dict[str, str] | None = None,
        extra: dict[str, Any] | None = None,
    ):
        """Initialize invalid API key error."""
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_type="invalid_api_key",
            headers=headers,
            extra=extra,
        )


class MissingAPIKeyError(AuthError):
    """Error raised when no API key is provided."""

    def __init__(
        self,
        detail: str = "No API key provided",
        headers: dict[str, str] | None = None,
        extra: dict[str, Any] | None = None,
    ):
        """Initialize missing API key error."""
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_type="missing_api_key",
            headers=headers,
            extra=extra,
        )


class APIKeyRateLimitError(AuthError):
    """Error raised when API key rate limit is exceeded."""

    def __init__(
        self,
        detail: str = "API key rate limit exceeded",
        headers: dict[str, str] | None = None,
        extra: dict[str, Any] | None = None,
    ):
        """Initialize rate limit error."""
        super().__init__(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_type="rate_limit_exceeded",
            headers=headers,
            extra=extra,
        )


class APIKeyPermissionError(AuthError):
    """Error raised when API key lacks required permissions."""

    def __init__(
        self,
        detail: str = "API key lacks required permissions",
        headers: dict[str, str] | None = None,
        extra: dict[str, Any] | None = None,
    ):
        """Initialize permission error."""
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail=detail,
            error_type="insufficient_permissions",
            headers=headers,
            extra=extra,
        )
