from fastapi import APIRouter, Request, BackgroundTasks
from typing import List, Dict, Any
from utils.database import DatabaseError
from utils.read import get_all_jobs
import redis
import json
import asyncio
from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
redis_client = redis.StrictRedis(host='https://big-swan-adversely.ngrok-free.app', port=6379, db=0, decode_responses=True)
limiter = Limiter(key_func=get_remote_address)

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
        raise DatabaseError(str(e))

@router.get("/jobs", response_model=List[Dict[str, Any]])
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
        DatabaseError: If there's an error fetching jobs from the database.
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
    except DatabaseError as e:
        logger.error(f"Database error in get_jobs: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_jobs: {str(e)}")
        raise AppException(500, "Internal server error")
