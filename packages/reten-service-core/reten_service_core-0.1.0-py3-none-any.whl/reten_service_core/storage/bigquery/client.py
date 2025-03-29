"""
BigQuery client implementation.
"""

from functools import lru_cache
from typing import Any

from google.api_core import retry
from google.cloud import bigquery
from google.cloud.bigquery import (
    Client,
    DatasetReference,
    QueryJob,
    QueryJobConfig,
    ScalarQueryParameter,
    TableReference,
)
from google.oauth2 import service_account

from ...core.settings import get_settings


class BigQueryClient:
    """
    Client for interacting with BigQuery.

    This client provides a simplified interface for common BigQuery operations
    with built-in retry logic and error handling.

    Example:
        ```python
        from reten_service_core.storage.bigquery import BigQueryClient

        # Create client
        client = BigQueryClient()

        # Execute query
        results = client.execute_query(
            "SELECT * FROM `project.dataset.table` LIMIT 10"
        )

        # Process results
        for row in results:
            print(row)
        ```
    """

    def __init__(
        self,
        project_id: str | None = None,
        credentials_path: str | None = None,
        location: str = "US",
        retry_timeout: float = 30.0,
    ) -> None:
        """
        Initialize the BigQuery client.

        Args:
            project_id: Optional project ID (defaults to settings)
            credentials_path: Optional path to service account credentials
            location: BigQuery location (defaults to US)
            retry_timeout: Timeout for retry operations in seconds
        """
        settings = get_settings()
        self.project_id = project_id or settings.gcp_project_id
        self.credentials_path = credentials_path or settings.gcp_service_account_path
        self.location = location
        self.retry_timeout = retry_timeout
        self._client = self._create_client()

    def _create_client(self) -> Client:
        """
        Create the underlying BigQuery client.

        Returns:
            Configured BigQuery client
        """
        if self.credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            return bigquery.Client(
                project=self.project_id,
                credentials=credentials,
                location=self.location,
            )
        return bigquery.Client(project=self.project_id, location=self.location)

    @retry.Retry(timeout=30.0)
    def execute_query(
        self,
        query: str,
        params: dict[str, Any] | None = None,
        job_config: QueryJobConfig | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Execute a BigQuery SQL query.

        Args:
            query: The SQL query to execute
            params: Optional query parameters
            job_config: Optional job configuration
            **kwargs: Additional arguments passed to query_job.result()

        Returns:
            List of rows as dictionaries

        Raises:
            google.api_core.exceptions.GoogleAPIError: On query execution error
        """
        config = job_config or QueryJobConfig()
        if params:
            config.query_parameters = [
                ScalarQueryParameter(name, "STRING", value) for name, value in params.items()
            ]

        query_job: QueryJob = self._client.query(
            query,
            job_config=config,
            retry=retry.Retry(timeout=self.retry_timeout),
        )

        # Wait for the query to complete
        results = query_job.result(**kwargs)

        # Convert to list of dicts
        return [dict(row.items()) for row in results]

    def get_table(
        self,
        dataset_id: str,
        table_id: str,
    ) -> TableReference:
        """
        Get a reference to a BigQuery table.

        Args:
            dataset_id: The dataset ID
            table_id: The table ID

        Returns:
            Reference to the table
        """
        dataset_ref = DatasetReference(self.project_id, dataset_id)
        return dataset_ref.table(table_id)

    def get_dataset(self, dataset_id: str) -> DatasetReference:
        """
        Get a reference to a BigQuery dataset.

        Args:
            dataset_id: The dataset ID

        Returns:
            Reference to the dataset
        """
        return DatasetReference(self.project_id, dataset_id)

    def table_exists(self, dataset_id: str, table_id: str) -> bool:
        """
        Check if a table exists.

        Args:
            dataset_id: The dataset ID
            table_id: The table ID

        Returns:
            True if the table exists, False otherwise
        """
        try:
            self._client.get_table(self.get_table(dataset_id, table_id))
            return True
        except Exception:  # We catch all exceptions as the table doesn't exist
            return False

    def dataset_exists(self, dataset_id: str) -> bool:
        """
        Check if a dataset exists.

        Args:
            dataset_id: The dataset ID

        Returns:
            True if the dataset exists, False otherwise
        """
        try:
            self._client.get_dataset(self.get_dataset(dataset_id))
            return True
        except Exception:  # We catch all exceptions as the dataset doesn't exist
            return False


@lru_cache
def get_bigquery_client(
    project_id: str | None = None,
    credentials_path: str | None = None,
    location: str = "US",
    retry_timeout: float = 30.0,
) -> BigQueryClient:
    """
    Get a cached BigQuery client instance.

    This function caches the client to avoid creating multiple instances.

    Args:
        project_id: Optional project ID (defaults to settings)
        credentials_path: Optional path to service account credentials
        location: BigQuery location (defaults to US)
        retry_timeout: Timeout for retry operations in seconds

    Returns:
        Cached BigQuery client instance
    """
    return BigQueryClient(
        project_id=project_id,
        credentials_path=credentials_path,
        location=location,
        retry_timeout=retry_timeout,
    )
