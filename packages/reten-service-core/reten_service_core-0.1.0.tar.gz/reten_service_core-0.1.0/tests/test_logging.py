"""
Tests for the logging module.
"""

import json
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from reten_service_core.core.settings import Settings
from reten_service_core.logging.config import JSONFormatter, RequestContextFilter, configure_logging


@pytest.fixture(autouse=True)
def setup_environment():
    """Set up environment variables required for tests."""
    os.environ["VALID_API_KEYS"] = json.dumps(["test-key"])
    os.environ["GCP_PROJECT_ID"] = "test-project"
    yield
    del os.environ["VALID_API_KEYS"]
    del os.environ["GCP_PROJECT_ID"]


@pytest.fixture
def test_settings():
    """Fixture for test settings."""
    return Settings(
        valid_api_keys=["test-key"],
        gcp_project_id="test-project",
        log_format="json",
        log_level="INFO",
    )


@pytest.fixture
def log_record() -> logging.LogRecord:
    """Create a test log record."""
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.module = "test_module"
    record.funcName = "test_function"
    record.process = 12345
    record.thread = 67890
    return record


@pytest.fixture
def json_formatter() -> JSONFormatter:
    """Create a JSON formatter instance."""
    return JSONFormatter()


@pytest.fixture
def temp_log_file(tmp_path: Path) -> str:
    """Create a temporary log file path."""
    return str(tmp_path / "test.log")


def test_json_formatter_basic(json_formatter: JSONFormatter, log_record: logging.LogRecord):
    """Test basic JSON formatting."""
    formatted = json_formatter.format(log_record)
    data = json.loads(formatted)

    assert data["level"] == "INFO"
    assert data["message"] == "Test message"
    assert data["module"] == "test_module"
    assert data["function"] == "test_function"
    assert data["line"] == 42
    assert data["process"] == 12345
    assert data["thread"] == 67890


def test_json_formatter_with_context(json_formatter: JSONFormatter, log_record: logging.LogRecord):
    """Test JSON formatting with request context."""
    log_record.request_id = "req-123"
    log_record.correlation_id = "corr-456"
    log_record.user_id = "user-789"
    log_record.duration_ms = 123.45
    log_record.status_code = 200

    formatted = json_formatter.format(log_record)
    data = json.loads(formatted)

    assert data["request_id"] == "req-123"
    assert data["correlation_id"] == "corr-456"
    assert data["user_id"] == "user-789"
    assert data["duration_ms"] == 123.45
    assert data["status_code"] == 200


def test_json_formatter_with_exception(
    json_formatter: JSONFormatter, log_record: logging.LogRecord
):
    """Test JSON formatting with exception info."""
    try:
        raise ValueError("Test error")
    except ValueError:
        log_record.exc_info = sys.exc_info()
        log_record.exc_text = "Test error traceback"

    formatted = json_formatter.format(log_record)
    data = json.loads(formatted)

    assert "exception" in data
    assert "exc_text" in data
    assert "Test error" in data["exception"]


def test_json_formatter_with_extra(json_formatter: JSONFormatter, log_record: logging.LogRecord):
    """Test JSON formatting with extra attributes."""
    log_record.extra = {
        "custom_field": "custom_value",
        "nested": {"key": "value"},
    }

    formatted = json_formatter.format(log_record)
    data = json.loads(formatted)

    assert data["custom_field"] == "custom_value"
    assert data["nested"] == {"key": "value"}


def test_request_context_filter():
    """Test request context filter."""
    context_filter = RequestContextFilter(request_id="default-id")
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # Test with no request_id
    assert context_filter.filter(record)
    assert record.request_id == "default-id"

    # Test with existing request_id
    record.request_id = "custom-id"
    assert context_filter.filter(record)
    assert record.request_id == "custom-id"


def test_configure_logging_basic():
    """Test basic logging configuration."""
    configure_logging(log_level="DEBUG", json_format=True)
    logger = logging.getLogger("test_logger")

    assert logger.getEffectiveLevel() == logging.DEBUG
    assert len(logger.handlers) == 0  # Root logger has the handlers

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.StreamHandler)
    assert isinstance(root_logger.handlers[0].formatter, JSONFormatter)


def test_configure_logging_with_file(temp_log_file: str):
    """Test logging configuration with file handler."""
    configure_logging(
        log_level="INFO",
        json_format=False,
        add_file_handler=True,
        log_file=temp_log_file,
    )
    logger = logging.getLogger("test_logger")
    logger.info("Test message")

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 2
    assert isinstance(root_logger.handlers[1], logging.FileHandler)

    # Check file content
    with open(temp_log_file) as f:
        log_content = f.read()
        assert "Test message" in log_content


def test_configure_logging_json_output():
    """Test JSON output in logging configuration."""
    configure_logging(log_level="INFO", json_format=True)
    logger = logging.getLogger("test_logger")

    # Capture log output
    with LogCapture() as log_output:
        logger.info(
            "Test message",
            extra={
                "request_id": "req-123",
                "user_id": "user-456",
                "duration_ms": 123.45,
            },
        )

        log_data = json.loads(log_output.records[0])
        assert log_data["message"] == "Test message"
        assert log_data["request_id"] == "req-123"
        assert log_data["user_id"] == "user-456"
        assert log_data["duration_ms"] == 123.45


class LogCapture:
    """Context manager to capture log output."""

    def __init__(self):
        """Initialize the log capture."""
        self.records: list[str] = []

    def __enter__(self):
        """Set up the log capture."""
        self.handler = logging.StreamHandler(StreamToList(self.records))
        self.handler.setFormatter(JSONFormatter())
        logging.getLogger().addHandler(self.handler)
        return self

    def __exit__(self, *args: Any):
        """Clean up the log capture."""
        logging.getLogger().removeHandler(self.handler)


class StreamToList:
    """Stream that writes to a list."""

    def __init__(self, records: list[str]):
        """Initialize the stream."""
        self.records = records

    def write(self, text: str):
        """Write to the list."""
        if text.strip():
            self.records.append(text.strip())

    def flush(self):
        """Flush the stream."""
        pass
