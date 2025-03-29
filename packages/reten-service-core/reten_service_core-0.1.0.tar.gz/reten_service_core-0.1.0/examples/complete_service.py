"""
Complete service example demonstrating all core components working together.

This example shows:
1. FastAPI service with API Key authentication
2. Structured logging with request context
3. BigQuery integration for data operations
4. Error handling and middleware
5. Settings configuration
6. Health checks and metrics
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from reten_service_core.auth import APIKeyAuth
from reten_service_core.core.settings import Settings
from reten_service_core.logging.config import configure_logging
from reten_service_core.storage.bigquery import get_bigquery_client


class MetricsResponse(BaseModel):
    """Response model for metrics endpoint."""

    start_date: datetime
    end_date: datetime
    total_records: int
    metrics: dict[str, Any]


def setup_app() -> FastAPI:
    """Initialize and configure the FastAPI application."""
    # Configure settings
    _ = Settings(
        VALID_API_KEYS=["test-key"],
        GCP_PROJECT_ID="your-project-id",
        GCP_SERVICE_ACCOUNT_PATH="/path/to/credentials.json",
        LOG_FORMAT="json",
        LOG_LEVEL="INFO",
    )

    # Configure logging
    configure_logging()

    # Create FastAPI app
    app = FastAPI(
        title="Complete Service Example",
        description="Example service using all core components",
        version="1.0.0",
    )

    # Add authentication
    app.add_middleware(APIKeyAuth)

    return app


app = setup_app()


@app.middleware("http")
async def log_requests(request: Request, call_next: Any) -> Any:
    """Log request and response details."""
    start_time = datetime.now()

    response = await call_next(request)

    # Calculate request duration
    duration = (datetime.now() - start_time).total_seconds()

    # Log request details
    logging.info(
        "Request processed",
        extra={
            "path": request.url.path,
            "method": request.method,
            "duration": duration,
            "status_code": response.status_code,
        },
    )

    return response


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    days: int = 7,
    dataset_id: str = "analytics",
    table_id: str = "events",
) -> MetricsResponse:
    """
    Get metrics from BigQuery.

    Args:
        days: Number of days to look back
        dataset_id: BigQuery dataset ID
        table_id: BigQuery table ID

    Returns:
        MetricsResponse with aggregated metrics
    """
    try:
        client = get_bigquery_client()

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Query for metrics
        query = f"""
        SELECT
            COUNT(*) as total_events,
            COUNT(DISTINCT user_id) as unique_users,
            AVG(duration) as avg_duration
        FROM `{client.project_id}.{dataset_id}.{table_id}`
        WHERE timestamp BETWEEN @start_date AND @end_date
        """

        results = client.execute_query(
            query,
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )

        if not results:
            raise ValueError("No results returned from query")

        # Log success
        logging.info(
            "Metrics retrieved successfully",
            extra={
                "dataset": dataset_id,
                "table": table_id,
                "days": days,
            },
        )

        # Return formatted response
        return MetricsResponse(
            start_date=start_date,
            end_date=end_date,
            total_records=len(results),
            metrics=results[0],
        )

    except Exception as e:
        # Log error with context
        logging.error(
            "Failed to retrieve metrics",
            extra={
                "error": str(e),
                "dataset": dataset_id,
                "table": table_id,
                "days": days,
            },
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve metrics",
        ) from e


if __name__ == "__main__":
    import uvicorn

    # Run the service
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,  # Disable uvicorn's logging config
    )
