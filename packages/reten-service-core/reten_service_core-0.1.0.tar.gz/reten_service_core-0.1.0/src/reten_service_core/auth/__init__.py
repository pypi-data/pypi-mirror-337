"""
Authentication module.
"""

from .api_key import APIKeyAuth, get_api_key
from .exceptions import (
    APIKeyPermissionError,
    APIKeyRateLimitError,
    AuthError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
)

__all__ = [
    "APIKeyAuth",
    "get_api_key",
    "AuthError",
    "InvalidAPIKeyError",
    "MissingAPIKeyError",
    "APIKeyRateLimitError",
    "APIKeyPermissionError",
]
