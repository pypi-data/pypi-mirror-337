# BigQuery Module

This module provides a simplified interface for interacting with Google BigQuery.

## Features

- Automatic configuration from settings
- Service account authentication support
- Query execution with parameter support
- Dataset and table management utilities
- Built-in retry logic and error handling

## Installation

The BigQuery module is part of the Reten Service Core library. Make sure you have the required dependencies:

```bash
pip install google-cloud-bigquery>=3.11.0
```

## Configuration

Configure the BigQuery client through environment variables or settings:

```python
from reten_service_core.core.settings import Settings

settings = Settings(
    gcp_project_id="your-project-id",
    gcp_service_account_path="/path/to/credentials.json",  # Optional
)
```

## Usage

### Basic Query

```python
from reten_service_core.storage.bigquery import get_bigquery_client

# Get a cached client instance
client = get_bigquery_client()

# Execute a query
results = client.execute_query(
    "SELECT * FROM `project.dataset.table` LIMIT 10"
)

# Process results
for row in results:
    print(row)
```

### Query with Parameters

```python
results = client.execute_query(
    """
    SELECT *
    FROM `project.dataset.table`
    WHERE timestamp >= @start_date
    """,
    params={
        "start_date": "2024-01-01",
    },
)
```

### Dataset and Table Operations

```python
# Check if dataset exists
if client.dataset_exists("my_dataset"):
    print("Dataset exists")

# Check if table exists
if client.table_exists("my_dataset", "my_table"):
    print("Table exists")

# Get dataset reference
dataset_ref = client.get_dataset("my_dataset")

# Get table reference
table_ref = client.get_table("my_dataset", "my_table")
```

### Custom Configuration

```python
from reten_service_core.storage.bigquery import BigQueryClient

# Create a client with custom settings
client = BigQueryClient(
    project_id="custom-project",
    credentials_path="/path/to/credentials.json",
    location="US",
    retry_timeout=30.0,
)
```

## Error Handling

The client includes built-in retry logic for transient errors. For other errors, use standard Python exception handling:

```python
try:
    results = client.execute_query("SELECT * FROM `project.dataset.table`")
except Exception as e:
    print(f"Query failed: {e}")
```

## Best Practices

1. Use the `get_bigquery_client()` function to get a cached client instance
2. Always provide query parameters instead of string formatting for security
3. Check for dataset and table existence before querying
4. Use appropriate error handling for production code
5. Configure logging to track query execution and errors

## Example

See the [BigQuery example](../../../examples/bigquery_example.py) for a complete working example.
