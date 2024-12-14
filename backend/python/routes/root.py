from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from utils.logger import get_logger
from utils.security import validate_input

logger = get_logger(__name__)
router = APIRouter()

@router.get("/", response_class=RedirectResponse)
def main(request: Request,_: None = Depends(validate_input)) -> RedirectResponse:
    session = request.session
    
    # Check if the session already has a username
    if "username" not in session:
        # Set a new session value (e.g., a default username)
        session["username"] = "Guest"  # You can set this to any default value or logic
        return RedirectResponse(url='/metrics')
    

    """
    Redirect to API documentation.

    Returns:
        RedirectResponse: Redirects to the API documentation page.
    """
    logger.info("Redirecting to API documentation")
    return RedirectResponse(url='/docs')
