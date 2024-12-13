from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/", response_class=RedirectResponse)
def main() -> RedirectResponse:
    """
    Redirect to API documentation.

    Returns:
        RedirectResponse: Redirects to the API documentation page.
    """
    logger.info("Redirecting to API documentation")
    return RedirectResponse(url='/docs')
