"""
Tests for the BigQuery client module.
"""

from unittest.mock import MagicMock, patch

import pytest
from google.auth.credentials import Credentials
from google.cloud.bigquery import (
    Client,
    DatasetReference,
    QueryJobConfig,
    ScalarQueryParameter,
    TableReference,
)

from reten_service_core.core.settings import Settings
from reten_service_core.storage.bigquery import BigQueryClient, get_bigquery_client


@pytest.fixture(autouse=True)
def test_settings():
    """Test settings fixture that is automatically used."""
    with patch("reten_service_core.storage.bigquery.client.get_settings") as mock:
        mock.return_value = Settings(
            VALID_API_KEYS=["test-key"],
            GCP_PROJECT_ID="test-project",
            GCP_SERVICE_ACCOUNT_PATH=None,
            LOG_FORMAT="json",
            LOG_LEVEL="INFO",
        )
        yield mock.return_value


@pytest.fixture
def mock_client():
    """Mock BigQuery client fixture."""
    with patch("google.cloud.bigquery.Client", autospec=True) as mock:
        mock.return_value = MagicMock(spec=Client)
        yield mock


@pytest.fixture
def mock_credentials():
    """Mock service account credentials fixture."""
    with patch("google.oauth2.service_account.Credentials", autospec=True) as mock:
        mock.from_service_account_file.return_value = MagicMock(spec=Credentials)
        yield mock


def test_client_init_default(test_settings, mock_client):
    """Test client initialization with default settings."""
    client = BigQueryClient()
    assert client.project_id == "test-project"
    assert client.credentials_path is None
    assert client.location == "US"
    assert client.retry_timeout == 30.0

    mock_client.assert_called_once_with(
        project="test-project",
        location="US",
    )


def test_client_init_with_service_account(test_settings, mock_client, mock_credentials):
    """Test client initialization with service account."""
    test_settings.gcp_service_account_path = "/path/to/credentials.json"
    client = BigQueryClient()
    assert client.project_id == "test-project"
    assert client.credentials_path == "/path/to/credentials.json"

    mock_credentials.from_service_account_file.assert_called_once_with(
        "/path/to/credentials.json",
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    mock_client.assert_called_once_with(
        project="test-project",
        credentials=mock_credentials.from_service_account_file.return_value,
        location="US",
    )


def test_execute_query(test_settings, mock_client):
    """Test query execution."""
    # Setup mock query job
    mock_job = MagicMock()
    mock_results = [
        {"name": "test1", "value": 1},
        {"name": "test2", "value": 2},
    ]
    mock_rows = []
    for row in mock_results:
        mock_row = MagicMock()
        mock_row.items.return_value = row.items()
        mock_rows.append(mock_row)
    mock_job.result.return_value = mock_rows
    mock_client.return_value.query.return_value = mock_job

    # Create client and execute query
    client = BigQueryClient()
    results = client.execute_query(
        "SELECT * FROM `test.table`",
        params={"param": "value"},
    )

    # Verify results
    assert results == mock_results
    mock_client.return_value.query.assert_called_once()
    call_args = mock_client.return_value.query.call_args
    assert call_args[0][0] == "SELECT * FROM `test.table`"
    assert isinstance(call_args[1]["job_config"], QueryJobConfig)
    assert len(call_args[1]["job_config"].query_parameters) == 1
    param = call_args[1]["job_config"].query_parameters[0]
    assert isinstance(param, ScalarQueryParameter)
    assert param.name == "param"
    assert param.value == "value"
    assert "retry" in call_args[1]


def test_execute_query_no_params(test_settings, mock_client):
    """Test query execution without parameters."""
    # Setup mock query job
    mock_job = MagicMock()
    mock_results = [
        {"name": "test1", "value": 1},
        {"name": "test2", "value": 2},
    ]
    mock_rows = []
    for row in mock_results:
        mock_row = MagicMock()
        mock_row.items.return_value = row.items()
        mock_rows.append(mock_row)
    mock_job.result.return_value = mock_rows
    mock_client.return_value.query.return_value = mock_job

    # Create client and execute query without params
    client = BigQueryClient()
    results = client.execute_query("SELECT * FROM `test.table`")

    # Verify results
    assert results == mock_results
    mock_client.return_value.query.assert_called_once()
    call_args = mock_client.return_value.query.call_args
    assert call_args[0][0] == "SELECT * FROM `test.table`"
    assert isinstance(call_args[1]["job_config"], QueryJobConfig)
    assert call_args[1]["job_config"].query_parameters == []
    assert "retry" in call_args[1]


def test_execute_query_with_job_config(test_settings, mock_client):
    """Test query execution with custom job config."""
    # Setup mock query job
    mock_job = MagicMock()
    mock_results = [{"name": "test1", "value": 1}]
    mock_rows = []
    for row in mock_results:
        mock_row = MagicMock()
        mock_row.items.return_value = row.items()
        mock_rows.append(mock_row)
    mock_job.result.return_value = mock_rows
    mock_client.return_value.query.return_value = mock_job

    # Create custom job config
    custom_config = QueryJobConfig()
    custom_config.use_query_cache = False

    # Create client and execute query with custom config
    client = BigQueryClient()
    results = client.execute_query(
        "SELECT * FROM `test.table`",
        job_config=custom_config,
    )

    # Verify results
    assert results == mock_results
    mock_client.return_value.query.assert_called_once()
    call_args = mock_client.return_value.query.call_args
    assert call_args[0][0] == "SELECT * FROM `test.table`"
    assert call_args[1]["job_config"] is custom_config
    assert call_args[1]["job_config"].query_parameters == []
    assert "retry" in call_args[1]


def test_table_operations(test_settings, mock_client):
    """Test table operations."""
    client = BigQueryClient()

    # Test get_table
    table_ref = client.get_table("test_dataset", "test_table")
    assert isinstance(table_ref, TableReference)
    assert table_ref.dataset_id == "test_dataset"
    assert table_ref.table_id == "test_table"
    assert table_ref.project == "test-project"

    # Test table_exists - table exists
    mock_client.return_value.get_table.return_value = MagicMock()
    assert client.table_exists("test_dataset", "test_table") is True

    # Test table_exists - table does not exist
    mock_client.return_value.get_table.side_effect = Exception()
    assert client.table_exists("test_dataset", "test_table") is False


def test_dataset_operations(test_settings, mock_client):
    """Test dataset operations."""
    client = BigQueryClient()

    # Test get_dataset
    dataset_ref = client.get_dataset("test_dataset")
    assert isinstance(dataset_ref, DatasetReference)
    assert dataset_ref.dataset_id == "test_dataset"
    assert dataset_ref.project == "test-project"

    # Test dataset_exists - dataset exists
    mock_client.return_value.get_dataset.return_value = MagicMock()
    assert client.dataset_exists("test_dataset") is True

    # Test dataset_exists - dataset does not exist
    mock_client.return_value.get_dataset.side_effect = Exception()
    assert client.dataset_exists("test_dataset") is False


def test_get_bigquery_client_cache():
    """Test BigQuery client caching."""
    with patch("reten_service_core.storage.bigquery.client.BigQueryClient") as mock:
        # First call should create a new client
        mock.side_effect = lambda **kwargs: MagicMock(project_id=kwargs.get("project_id"))

        client1 = get_bigquery_client(project_id="test-project")
        assert mock.call_count == 1
        assert client1.project_id == "test-project"

        # Second call with same args should return cached client
        client2 = get_bigquery_client(project_id="test-project")
        assert mock.call_count == 1
        assert client1 == client2

        # Different args should create new client
        client3 = get_bigquery_client(project_id="other-project")
        assert mock.call_count == 2
        assert client3.project_id == "other-project"
        assert client1 != client3
