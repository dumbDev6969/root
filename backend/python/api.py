from fastapi import FastAPI, Query, Request, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from typing import List, Dict, Any
from utils.database import DatabaseError
from utils.create import create as db_create
from utils.read import read as db_read, get_all_jobs
from utils.update import update as db_update
from utils.delete import delete as db_delete
from routes import geo, signup, send_email, jobs, update, query_and_delete, contact
from routes.crud_routes import router as crud_router
from utils.email_sender import my_send_email
from utils.logger import get_logger
import redis
import json
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
import inspect

# Import our new models and middleware
from models import Srecruter, SignupRecruter, CreateRequest
from middleware import metrics_middleware, metrics

# Import error handling components
from utils.error_handler import setup_error_handlers, AppException, DatabaseException, ValidationException

# Set up logging
logger = get_logger(__name__)

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="JobSearch API",
    description="API for job search and recruitment operations",
    version="1.0.0",
)

# Set up error handlers
setup_error_handlers(app)

# Add rate limiting to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add metrics middleware
app.middleware("http")(metrics_middleware)

# Create a crud object with the necessary database operations
class CRUD:
    def __init__(self):
        self.create = db_create
        self.read = db_read
        self.update = db_update
        self.delete = db_delete
        self.get_all_jobs = get_all_jobs

crud = CRUD()

# Routes

@app.get("/", response_class=RedirectResponse)
def main() -> RedirectResponse:
    """
    Redirect to API documentation.

    Returns:
        RedirectResponse: Redirects to the API documentation page.
    """
    logger.info("Redirecting to API documentation")
    return RedirectResponse(url='/docs')

@app.get("/metrics")
async def get_metrics():
    """
    Retrieve application metrics.

    Returns:
        Response: Prometheus metrics in text format.
    """
    return await metrics()

async def fetch_jobs_from_db():
    """
    Fetch all jobs from the database asynchronously.

    Returns:
        List[Dict[str, Any]]: A list of job dictionaries.

    Raises:
        DatabaseException: If there's an error fetching jobs from the database.
    """
    try:
        logger.info("Fetching jobs from database")
        return await asyncio.to_thread(crud.get_all_jobs)
    except Exception as e:
        logger.error(f"Error fetching jobs from database: {str(e)}")
        raise DatabaseException(str(e))

@app.get("/jobs", response_model=List[Dict[str, Any]])
@limiter.limit("100/minute")
async def get_jobs(request: Request, background_tasks: BackgroundTasks) -> List[Dict[str, Any]]:
    """
    Retrieve all jobs from the database or cache.

    This endpoint is rate limited to 100 requests per minute.

    Args:
        request (Request): The incoming request object.
        background_tasks (BackgroundTasks): FastAPI background tasks object.

    Returns:
        List[Dict[str, Any]]: A list of job dictionaries.

    Raises:
        DatabaseException: If there's an error fetching jobs from the database.
        AppException: If there's an unexpected error.
    """
    logger.info("Received request to get all jobs")
    try:
        # Check if jobs data is cached
        cached_jobs = redis_client.get('jobs')
        if cached_jobs:
            logger.info("Returning cached jobs data")
            return json.loads(cached_jobs)

        # If not cached, fetch from database asynchronously
        logger.info("Fetching jobs data from database")
        jobs_data = await fetch_jobs_from_db()
        if jobs_data:
            # Use background task to cache the data
            background_tasks.add_task(redis_client.setex, 'jobs', 300, json.dumps(jobs_data))
            logger.info("Jobs data cached for 5 minutes")
        return jobs_data
    except DatabaseException as e:
        logger.error(f"Database error in get_jobs: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_jobs: {str(e)}")
        raise AppException(500, "Internal server error")

async def create_recruiter(table: str, data: Dict[str, Any]):
    """
    Create a new recruiter in the database.

    Args:
        table (str): The name of the table to insert the recruiter into.
        data (Dict[str, Any]): The recruiter data to insert.

    Returns:
        Any: The result of the database insertion.

    Raises:
        DatabaseException: If there's an error creating the recruiter in the database.
    """
    try:
        logger.info(f"Creating new recruiter: {data.get('email')}")
        return await asyncio.to_thread(crud.create, table, **data)
    except Exception as e:
        logger.error(f"Error creating recruiter: {str(e)}")
        raise DatabaseException(str(e))

@app.post("/signup", response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def signup_recruiter(request: Request, signup_data: SignupRecruter) -> Dict[str, Any]:
    """
    Sign up a new recruiter.

    This endpoint is rate limited to 10 requests per minute.

    Args:
        request (Request): The incoming request object.
        signup_data (SignupRecruter): The recruiter signup data.

    Returns:
        Dict[str, Any]: A dictionary containing a success message.

    Raises:
        DatabaseException: If there's an error creating the recruiter in the database.
        ValidationException: If there's a validation error with the signup data.
        AppException: If there's an unexpected error.
    """
    logger.info(f"Received signup request for recruiter: {signup_data.data.email}")
    try:
        await create_recruiter(signup_data.table, signup_data.data.dict())
        logger.info(f"Recruiter signed up successfully: {signup_data.data.email}")
        return {"message": "Recruiter signed up successfully"}
    except DatabaseException as e:
        logger.error(f"Database error in signup_recruiter: {str(e)}")
        raise
    except ValidationException as e:
        logger.error(f"Validation error in signup_recruiter: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in signup_recruiter: {str(e)}")
        raise AppException(500, "Internal server error")

# Include other route modules
modules_to_run = [
    (jobs, app),
    (geo, app),
    (signup, app),
    (send_email, app),
    (update, app),
    (query_and_delete, app),
    (contact, app)
]

for module, app_instance in modules_to_run:
    logger.info(f"Initializing module: {module.__name__}")
    if hasattr(module, 'run'):
        run_func = getattr(module, 'run')
        if 'crud' in inspect.signature(run_func).parameters:
            run_func(app_instance, crud)
        else:
            run_func(app_instance)
    else:
        logger.warning(f"Module {module.__name__} does not have a 'run' method")

app.include_router(crud_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the application")
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=11352,
        reload=True
    )
