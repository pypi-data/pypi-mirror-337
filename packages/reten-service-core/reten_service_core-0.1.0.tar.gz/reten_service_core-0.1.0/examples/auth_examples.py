"""
Ejemplos detallados de autenticación con API Key.

Este ejemplo muestra:
1. Configuración básica y avanzada del middleware
2. Exclusión de rutas
3. Personalización del header
4. Logging de intentos de autenticación
5. Manejo de errores personalizado
"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from reten_service_core.auth import (
    APIKeyAuth,
    APIKeyPermissionError,
    APIKeyRateLimitError,
    AuthError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    get_api_key,
)
from reten_service_core.core.settings import Settings
from reten_service_core.logging.config import configure_logging


def setup_app() -> FastAPI:
    """Initialize and configure the FastAPI application."""
    # Configure settings with multiple valid keys
    _ = Settings(
        VALID_API_KEYS=["test-key-1", "test-key-2"],
        GCP_PROJECT_ID="your-project-id",
        LOG_FORMAT="json",
        LOG_LEVEL="INFO",
    )

    # Configure logging
    configure_logging()

    # Create FastAPI app
    app = FastAPI(
        title="Auth Examples",
        description="Examples of API Key authentication configurations",
        version="1.0.0",
    )

    return app


# Create the base app
app = setup_app()

# Example 1: Basic Authentication
# This is the simplest setup, using all defaults
app.add_middleware(APIKeyAuth)


# Example 2: Custom Configuration
# Create a new FastAPI app with custom auth configuration
custom_app = FastAPI()
custom_app.add_middleware(
    APIKeyAuth,
    header_name="X-Custom-Key",  # Custom header name
    exclude_paths=["/public", "/health"],  # Additional excluded paths
    log_invalid_attempts=True,  # Log invalid authentication attempts
)


@app.get("/private")
async def private_endpoint(request: Request) -> dict[str, str]:
    """Endpoint that requires authentication."""
    # Get the validated API key
    api_key = get_api_key(request)
    return {
        "message": "This is a private endpoint",
        "key": api_key[:8] + "...",  # Show partial key safely
    }


@app.get("/public")
async def public_endpoint() -> dict[str, str]:
    """Endpoint that doesn't require authentication."""
    return {"message": "This is a public endpoint"}


@app.get("/error/missing")
async def missing_key_error() -> dict[str, str]:
    """Endpoint that demonstrates missing API key error."""
    raise MissingAPIKeyError(
        detail="API key must be provided in X-API-Key header",
        extra={"required_header": "X-API-Key"},
    )


@app.get("/error/invalid")
async def invalid_key_error() -> dict[str, str]:
    """Endpoint that demonstrates invalid API key error."""
    raise InvalidAPIKeyError(
        detail="The provided API key is not valid",
        extra={"reason": "key not found in valid keys"},
    )


@app.get("/error/permission")
async def permission_error() -> dict[str, str]:
    """Endpoint that demonstrates permission error."""
    raise APIKeyPermissionError(
        detail="API key lacks required permissions",
        extra={"required_permissions": ["read", "write"]},
    )


@app.get("/error/rate-limit")
async def rate_limit_error() -> dict[str, str]:
    """Endpoint that demonstrates rate limit error."""
    raise APIKeyRateLimitError(
        detail="Too many requests",
        headers={"Retry-After": "60"},
        extra={"limit": 100, "period": "1 minute"},
    )


@app.middleware("http")
async def custom_auth_handler(request: Request, call_next: Any) -> Any:
    """
    Custom middleware to handle authentication errors.

    This shows how to add custom handling on top of the API Key auth.
    """
    try:
        # Process the request
        response = await call_next(request)
        return response

    except AuthError as exc:
        # Log the error with context
        logging.error(
            "Authentication error",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": exc.error_type,
                "error": str(exc.detail),
                "status_code": exc.status_code,
                **exc.extra,  # Include any extra context
            },
        )

        # Return custom error response
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_type,
                "detail": exc.detail,
                "type": "authentication_error",
                **exc.extra,  # Include any extra context in response
            },
            headers=exc.headers,  # Include any custom headers
        )


if __name__ == "__main__":
    import uvicorn

    print("""
Auth Examples Server

Test the endpoints with:

1. Private endpoint (requires auth):
   curl -H "X-API-Key: test-key-1" http://localhost:8000/private

2. Private endpoint (invalid auth):
   curl -H "X-API-Key: invalid-key" http://localhost:8000/private

3. Public endpoint (no auth required):
   curl http://localhost:8000/public

4. Error examples:
   curl -H "X-API-Key: test-key-1" http://localhost:8000/error/missing
   curl -H "X-API-Key: test-key-1" http://localhost:8000/error/invalid
   curl -H "X-API-Key: test-key-1" http://localhost:8000/error/permission
   curl -H "X-API-Key: test-key-1" http://localhost:8000/error/rate-limit
""")

    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,  # Disable uvicorn's logging config
    )
