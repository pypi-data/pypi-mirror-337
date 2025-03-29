"""
Example demonstrating the usage of the BigQuery client.

This example shows how to:
1. Initialize the client
2. Execute queries with parameters
3. Check for dataset/table existence
4. Handle errors
"""

import logging
from typing import Any

from reten_service_core.core.settings import Settings
from reten_service_core.logging.config import configure_logging
from reten_service_core.storage.bigquery import get_bigquery_client


def setup_logging() -> None:
    """Configure logging for the example."""
    configure_logging(
        log_level="INFO",
        json_format=False,
    )


def query_data(dataset_id: str, table_id: str) -> list[dict[str, Any]]:
    """
    Query data from a BigQuery table.

    Args:
        dataset_id: The dataset ID
        table_id: The table ID

    Returns:
        List of rows as dictionaries
    """
    client = get_bigquery_client()

    # Check if dataset and table exist
    if not client.dataset_exists(dataset_id):
        raise ValueError(f"Dataset {dataset_id} does not exist")
    if not client.table_exists(dataset_id, table_id):
        raise ValueError(f"Table {dataset_id}.{table_id} does not exist")

    # Execute query with parameters
    query = f"""
    SELECT *
    FROM `{client.project_id}.{dataset_id}.{table_id}`
    WHERE timestamp >= @start_date
    LIMIT 10
    """

    try:
        results = client.execute_query(
            query,
            params={
                "start_date": "2024-01-01",
            },
        )
        logging.info("Query executed successfully", extra={"row_count": len(results)})
        return results
    except Exception as e:
        logging.error("Query execution failed", extra={"error": str(e)})
        raise


def main() -> None:
    """Run the example."""
    # Configure settings and logging
    _ = Settings(  # Settings are automatically used by get_settings()
        valid_api_keys=["test-key"],
        gcp_project_id="your-project-id",
        gcp_service_account_path="/path/to/credentials.json",
        log_format="standard",
        log_level="INFO",
    )
    setup_logging()

    try:
        # Query data
        results = query_data("your_dataset", "your_table")

        # Process results
        for row in results:
            logging.info("Processing row", extra={"row": row})
    except Exception as e:
        logging.error("Example failed", extra={"error": str(e)})
        raise


if __name__ == "__main__":
    main()
