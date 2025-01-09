from fastapi import APIRouter, Depends
from utils.logger import get_logger
from utils.security import validate_input
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from fastapi.responses import Response

logger = get_logger(__name__)
router = APIRouter()

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

async def metrics():
    """Generate Prometheus metrics."""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@router.get("/metrics")
async def get_metrics(_: None = Depends(validate_input)):
    """
    Retrieve application metrics.

    Returns:
        Response: Prometheus metrics in text format.
    """
    return await metrics()
