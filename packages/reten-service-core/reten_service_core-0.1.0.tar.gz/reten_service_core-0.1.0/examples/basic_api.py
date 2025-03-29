"""
Basic API example using the service core library.
"""

from fastapi import FastAPI

from reten_service_core.auth import APIKeyAuth
from reten_service_core.logging import configure_logging

# Configure logging
configure_logging()

# Create FastAPI app
app = FastAPI(
    title="Example API",
    description="Example API using service core library",
    version="1.0.0",
)

# Add authentication
app.add_middleware(APIKeyAuth)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
