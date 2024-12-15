from fastapi import HTTPException, Request
from .validator import detect_html_and_sql_injection
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def validate_input(request: Request):
    # Get the request body as a string
    body = await request.body()
    body_str = body.decode()

    # Get query parameters as a string
    query_params = str(request.query_params)

    # Combine body and query params for validation
    input_str = body_str + query_params

    # Log the input being validated
    logging.debug(f"Validating input: {input_str}")

    # Detect potential threats
    detection_results = detect_html_and_sql_injection(input_str)

    if detection_results['has_html_tags'] or detection_results['has_sql_injection']:
        logging.warning(f"Potential threat detected: {detection_results}")
        raise HTTPException(status_code=400, detail="Potential security threat detected in the input")

    # If no threats detected, return None (request can proceed)
    return None
