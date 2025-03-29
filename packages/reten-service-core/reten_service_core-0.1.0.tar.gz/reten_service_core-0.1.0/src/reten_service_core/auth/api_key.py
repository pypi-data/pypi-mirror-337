"""
API Key authentication middleware and utilities.

This module provides middleware for API key authentication in FastAPI applications.
It validates API keys from request headers against a configured list of valid keys.
"""

import logging

from fastapi import Request
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from ..core.settings import get_settings
from .exceptions import (
    InvalidAPIKeyError,
    MissingAPIKeyError,
)

logger = logging.getLogger(__name__)


class APIKeyAuth(BaseHTTPMiddleware):
    """
    Middleware for API Key authentication.

    This middleware validates the API key in the request header against
    the configured valid keys. It supports excluding specific paths from
    authentication and customizing the header name.

    Example:
        ```python
        from fastapi import FastAPI
        from reten_service_core.auth import APIKeyAuth

        app = FastAPI()

        # Basic usage
        app.add_middleware(APIKeyAuth)

        # Custom configuration
        app.add_middleware(
            APIKeyAuth,
            header_name="X-Custom-Key",
            exclude_paths=["/health", "/metrics"],
            log_invalid_attempts=True,
        )
        ```

    Attributes:
        header_name: Name of the header containing the API key
        exclude_paths: List of paths excluded from authentication
        log_invalid_attempts: Whether to log invalid authentication attempts
    """

    def __init__(
        self,
        app,
        header_name: str = "X-API-Key",
        exclude_paths: list[str] | None = None,
        log_invalid_attempts: bool = False,
    ):
        """
        Initialize the API Key authentication middleware.

        Args:
            app: The FastAPI application
            header_name: The name of the header containing the API key
            exclude_paths: List of paths to exclude from authentication
            log_invalid_attempts: Whether to log invalid authentication attempts
        """
        super().__init__(app)
        self.header_name = header_name
        self.api_key_header = APIKeyHeader(name=header_name, auto_error=False)
        self.exclude_paths = exclude_paths or ["/docs", "/redoc", "/openapi.json"]
        self.log_invalid_attempts = log_invalid_attempts
        self.settings = get_settings()

    def is_path_excluded(self, path: str) -> bool:
        """
        Check if a path is excluded from authentication.

        Args:
            path: The request path to check

        Returns:
            True if the path is excluded, False otherwise
        """
        return any(path.startswith(excluded) for excluded in self.exclude_paths)

    def is_valid_api_key(self, api_key: str | None) -> bool:
        """
        Validate an API key against the configured valid keys.

        Args:
            api_key: The API key to validate

        Returns:
            True if the key is valid, False otherwise
        """
        return bool(api_key and api_key in self.settings.valid_api_keys)

    def log_auth_attempt(
        self,
        request: Request,
        error_type: str,
        error_detail: str,
        extra: dict | None = None,
    ) -> None:
        """
        Log an authentication attempt.

        Args:
            request: The request being authenticated
            error_type: Type of error encountered
            error_detail: Detailed error message
            extra: Additional context to log
        """
        if not self.log_invalid_attempts:
            return

        log_data = {
            "path": request.url.path,
            "method": request.method,
            "client_host": request.client.host if request.client else None,
            "error_type": error_type,
            "error_detail": error_detail,
        }
        if extra:
            log_data.update(extra)

        logger.warning("Authentication failed", extra=log_data)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process the request and validate the API key.

        This method:
        1. Checks if the path is excluded from authentication
        2. Extracts the API key from the request header
        3. Validates the API key
        4. Optionally logs invalid attempts
        5. Returns the appropriate response

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response from the next middleware or an error response

        Raises:
            MissingAPIKeyError: When no API key is provided
            InvalidAPIKeyError: When an invalid API key is provided
            APIKeyPermissionError: When the API key lacks required permissions
            APIKeyRateLimitError: When rate limits are exceeded
        """
        # Skip authentication for excluded paths
        if self.is_path_excluded(request.url.path):
            return await call_next(request)

        try:
            # Extract API key
            api_key = await self.api_key_header(request)
            if not api_key:
                raise MissingAPIKeyError(detail=f"No API key provided in {self.header_name} header")

            # Validate API key
            if not self.is_valid_api_key(api_key):
                raise InvalidAPIKeyError(
                    detail="Invalid API key",
                    extra={"provided_key": api_key[:8] + "..."},  # Log partial key safely
                )

            # Add API key to request state for downstream use
            request.state.api_key = api_key
            return await call_next(request)

        except (MissingAPIKeyError, InvalidAPIKeyError) as exc:
            self.log_auth_attempt(
                request=request,
                error_type=exc.error_type,
                error_detail=exc.detail,
                extra=exc.extra,
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": exc.error_type,
                    "detail": exc.detail,
                    "type": "authentication_error",
                },
            )


def get_api_key(request: Request) -> str:
    """
    Get the validated API key from the request state.

    This helper function can be used in route handlers to access
    the API key that was validated by the middleware.

    Args:
        request: The request object

    Returns:
        The validated API key

    Example:
        ```python
        from fastapi import FastAPI, Request
        from reten_service_core.auth import get_api_key

        app = FastAPI()
        app.add_middleware(APIKeyAuth)

        @app.get("/protected")
        async def protected_route(request: Request):
            api_key = get_api_key(request)
            return {"message": "Access granted", "key": api_key}
        ```
    """
    return request.state.api_key
