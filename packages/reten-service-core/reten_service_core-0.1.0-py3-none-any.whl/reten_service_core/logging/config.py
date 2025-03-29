"""
Logging configuration module.

This module provides a standardized logging configuration for Reten services.
It supports both JSON and standard formatting, with customizable handlers and levels.
"""

import json
import logging
import logging.config
import sys
from typing import Any

from ..core.settings import get_settings


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for log records.

    This formatter outputs log records in JSON format for better
    parsing in log aggregation systems.

    Example:
        ```python
        {
            "timestamp": "2024-03-27 12:34:56,789",
            "level": "INFO",
            "message": "Request processed",
            "module": "api",
            "function": "process_request",
            "request_id": "123e4567-e89b-12d3-a456-426614174000",
            "duration_ms": 123.45,
            "status_code": 200
        }
        ```
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as JSON.

        Args:
            record: The log record to format

        Returns:
            The formatted log record as a JSON string
        """
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }

        # Add request context if available
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        # Add performance metrics if available
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            log_data["exc_text"] = record.exc_text

        # Add any extra attributes
        if hasattr(record, "extra"):
            extra_data = getattr(record, "extra", {})
            log_data.update(extra_data)

        return json.dumps(log_data)


class RequestContextFilter(logging.Filter):
    """
    Filter that adds request context to log records.

    This filter is used to add request-specific information to log records,
    such as request_id, user_id, etc.
    """

    def __init__(self, request_id: str | None = None):
        """
        Initialize the filter with optional default values.

        Args:
            request_id: Optional default request ID
        """
        super().__init__()
        self.default_request_id = request_id

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request context to the log record if not already present.

        Args:
            record: The log record to modify

        Returns:
            True to include the record in the output
        """
        if not hasattr(record, "request_id"):
            record.request_id = self.default_request_id
        return True


def configure_logging(
    log_level: str | None = None,
    json_format: bool | None = None,
    add_file_handler: bool = False,
    log_file: str | None = None,
) -> None:
    """
    Configure the logging system.

    This function sets up logging with either JSON or standard formatting
    based on the application settings or provided parameters.

    Args:
        log_level: Override the log level from settings
        json_format: Override the JSON format setting
        add_file_handler: Whether to add a file handler
        log_file: Path to the log file if file handler is enabled

    Example:
        ```python
        from reten_service_core.logging import configure_logging

        # Basic configuration
        configure_logging()

        # With file logging
        configure_logging(
            log_level="DEBUG",
            json_format=True,
            add_file_handler=True,
            log_file="app.log"
        )

        # Use the logger
        logger = logging.getLogger(__name__)
        logger.info("Application started", extra={
            "request_id": "123",
            "user_id": "user-456",
            "duration_ms": 123.45
        })
        ```
    """
    settings = get_settings()

    # Use parameters or fall back to settings
    level = log_level or settings.log_level
    use_json = json_format if json_format is not None else settings.log_format == "json"

    config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {
            "request_context": {
                "()": RequestContextFilter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "json" if use_json else "standard",
                "filters": ["request_context"],
            },
        },
        "root": {
            "handlers": ["console"],
            "level": level.upper(),
        },
    }

    # Add file handler if requested
    if add_file_handler and log_file:
        config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "filename": log_file,
            "formatter": "json" if use_json else "standard",
            "filters": ["request_context"],
        }
        config["root"]["handlers"].append("file")

    logging.config.dictConfig(config)

    # Log initial configuration
    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured",
        extra={
            "log_level": level.upper(),
            "json_format": use_json,
            "handlers": config["root"]["handlers"],
        },
    )
