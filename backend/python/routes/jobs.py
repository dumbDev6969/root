from fastapi import APIRouter, Request, BackgroundTasks, Depends
from typing import List, Dict, Any
from utils.database import DatabaseError
from utils.read import get_all_jobs
from utils.error_handler import AppException, DatabaseException
import redis
import json
from datetime import datetime
import asyncio
from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.logger import get_logger
from utils.security import validate_input

logger = get_logger(__name__)
router = APIRouter()

# Initialize Redis with error handling
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
except redis.ConnectionError:
    logger.warning("Redis connection failed, caching will be disabled")
    redis_client = None

limiter = Limiter(key_func=get_remote_address)

def serialize_datetime(obj):
    """Helper function to serialize datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

async def fetch_jobs_from_db():
    """
    Fetch all jobs from the database asynchronously.

    Returns:
        List[Dict[str, Any]]: A list of job dictionaries.

    Raises:
        DatabaseError: If there's an error fetching jobs from the database.
    """
    try:
        logger.info("Fetching jobs from database")
        return await asyncio.to_thread(get_all_jobs)
    except Exception as e:
        logger.error(f"Error fetching jobs from database: {str(e)}")
        raise DatabaseException(str(e))

@router.get("/jobs", response_model=List[Dict[str, Any]])
@limiter.limit("100/minute")
async def get_jobs(request: Request, background_tasks: BackgroundTasks, _: None = Depends(validate_input)) -> List[Dict[str, Any]]:
    """
    Retrieve all jobs from the database or cache.

    This endpoint is rate limited to 100 requests per minute.

    Args:
        request (Request): The incoming request object.
        background_tasks (BackgroundTasks): FastAPI background tasks object.

    Returns:
        List[Dict[str, Any]]: A list of job dictionaries.

    Raises:
        DatabaseError: If there's an error fetching jobs from the database.
        AppException: If there's an unexpected error.
    """
    logger.info("Received request to get all jobs")
    try:
        # Check if Redis is available and jobs data is cached
        if redis_client:
            try:
                cached_jobs = redis_client.get('jobs')
                if cached_jobs:
                    logger.info("Returning cached jobs data")
                    return json.loads(cached_jobs)
            except redis.ConnectionError:
                logger.warning("Redis connection failed, falling back to database")

        # If not cached or Redis unavailable, fetch from database asynchronously
        logger.info("Fetching jobs data from database")
        jobs_data = await fetch_jobs_from_db()
        
        # Try to cache if Redis is available
        if redis_client and jobs_data:
            try:
                # Serialize with datetime handling
                serialized_data = json.dumps(jobs_data, default=serialize_datetime)
                background_tasks.add_task(redis_client.setex, 'jobs', 300, serialized_data)
                logger.info("Jobs data cached for 5 minutes")
            except redis.ConnectionError:
                logger.warning("Failed to cache jobs data")
            except TypeError as e:
                logger.error(f"Error serializing jobs data: {e}")
        
        return jobs_data
    except DatabaseException as e:
        logger.error(f"Database error in get_jobs: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_jobs: {str(e)}")
        raise AppException(500, "Internal server error")
