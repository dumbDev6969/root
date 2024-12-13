from fastapi import APIRouter
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    """
    Retrieve application metrics.

    Returns:
        Response: Prometheus metrics in text format.
    """
    return await metrics()
