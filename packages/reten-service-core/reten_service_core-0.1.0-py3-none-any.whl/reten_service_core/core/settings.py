"""
Core settings module.
"""

import json
from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Core settings for the application.

    This class defines all the configuration options available.
    Values are loaded from environment variables.
    """

    # API Authentication
    valid_api_keys: list[str] = Field(alias="VALID_API_KEYS")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")

    # BigQuery
    gcp_project_id: str = Field(alias="GCP_PROJECT_ID")
    gcp_service_account_path: str | None = Field(default=None, alias="GCP_SERVICE_ACCOUNT_PATH")

    # Project Info
    project_name: str = Field(default="Reten Service", alias="PROJECT_NAME")
    version: str = Field(default="0.1.0", alias="VERSION")
    description: str = Field(default="Reten Service Core", alias="DESCRIPTION")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        populate_by_name=True,
    )

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
        """Parse environment variables."""
        if field_name == "valid_api_keys":
            try:
                return json.loads(raw_val)
            except json.JSONDecodeError:
                return raw_val.split(",")
        return raw_val


@lru_cache
def get_settings() -> Settings:
    """
    Get the application settings.

    This function is cached to avoid reading the settings multiple times.

    Returns:
        The application settings
    """
    return Settings()
