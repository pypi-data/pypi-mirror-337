"""
BigQuery storage module for interacting with Google BigQuery.
"""

from .client import BigQueryClient, get_bigquery_client

__all__ = ["BigQueryClient", "get_bigquery_client"]
