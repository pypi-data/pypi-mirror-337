"""
Tests for the settings module.
"""

import os
from unittest.mock import patch

from reten_service_core.core.settings import Settings, get_settings


def test_get_settings():
    """Test that get_settings returns a Settings instance."""
    with patch.dict(
        os.environ,
        {
            "valid_api_keys": '["test-key"]',
            "gcp_project_id": "test-project",
            "log_format": "json",
        },
    ):
        settings = get_settings()
        assert isinstance(settings, Settings)
        assert settings.log_format == "json"
        assert settings.log_level == "INFO"
        assert settings.valid_api_keys == ["test-key"]
        assert settings.gcp_project_id == "test-project"
