from fastapi import FastAPI, Query, HTTPException, Request, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any
from utils.crud import CRUD, DatabaseError
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
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from starlette.responses import Response
import time

# Set up logging
logger = get_logger(__name__)

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize CRUD operations
crud = CRUD(
    host='localhost',
    user='root',
    password='',
    database='jobsearch'
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize Prometheus metrics
if 'request_count' not in REGISTRY._names_to_collectors:
    REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])
    REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])
    ACTIVE_REQUESTS = Gauge('active_requests', 'Active requests')
else:
    REQUEST_COUNT = REGISTRY._names_to_collectors['request_count']
    REQUEST_LATENCY = REGISTRY._names_to_collectors['request_latency_seconds']
    ACTIVE_REQUESTS = REGISTRY._names_to_collectors['active_requests']

app = FastAPI(
    title="JobSearch API",
    description="API for job search and recruitment operations",
    version="1.0.0",
)

# Add rate limiting to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Srecruter(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=20)
    state: str = Field(..., min_length=1, max_length=50)
    city_or_province: Optional[str] = Field(None, max_length=50)
    municipality: Optional[str] = Field(None, max_length=50)
    zip_code: str = Field(..., min_length=5, max_length=10)
    street_number: Optional[str] = Field(None, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    created_at: Optional[str]
    updated_at: Optional[str]

    @validator('phone_number')
    def validate_phone_number(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v

class SignupRecruter(BaseModel):
    table: str
    data: Srecruter

class CreateRequest(BaseModel):
    table: str
    data: Dict[str, Any]

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    ACTIVE_REQUESTS.dec()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
    logger.info(f"Request: {request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.2f}s")
    return response

@app.get("/metrics")
async def metrics():
    logger.info("Metrics endpoint accessed")
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/", response_class=RedirectResponse)
def main() -> RedirectResponse:
    """
    Redirect to API documentation
    """
    logger.info("Redirecting to API documentation")
    return RedirectResponse(url='/docs')

async def fetch_jobs_from_db():
    try:
        logger.info("Fetching jobs from database")
        return await asyncio.to_thread(crud.get_all_jobs)
    except Exception as e:
        logger.error(f"Error fetching jobs from database: {str(e)}")
        raise

@app.get("/jobs", response_model=List[Dict[str, Any]])
@limiter.limit("100/minute")
async def get_jobs(request: Request, background_tasks: BackgroundTasks) -> List[Dict[str, Any]]:
    """
    Retrieve all jobs from the database or cache

    This endpoint is rate limited to 100 requests per minute.
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
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        logger.error(f"Unexpected error in get_jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def create_recruiter(table: str, data: Dict[str, Any]):
    try:
        logger.info(f"Creating new recruiter: {data.get('email')}")
        return await asyncio.to_thread(crud.create, table, **data)
    except Exception as e:
        logger.error(f"Error creating recruiter: {str(e)}")
        raise

@app.post("/signup", response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def signup_recruiter(request: Request, signup_data: SignupRecruter) -> Dict[str, Any]:
    """
    Sign up a new recruiter

    This endpoint is rate limited to 10 requests per minute.
    """
    logger.info(f"Received signup request for recruiter: {signup_data.data.email}")
    try:
        await create_recruiter(signup_data.table, signup_data.data.dict())
        logger.info(f"Recruiter signed up successfully: {signup_data.data.email}")
        return {"message": "Recruiter signed up successfully"}
    except DatabaseError as e:
        logger.error(f"Database error in signup_recruiter: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to sign up recruiter")
    except Exception as e:
        logger.error(f"Unexpected error in signup_recruiter: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

modules_to_run = [
    (jobs, [app]),
    (geo, [app]),
    (signup, [app, crud]),
    (send_email, [app]),
    (update, [app, crud]),
    (query_and_delete, [app, crud]),
    (contact, [app])
]

for module, args in modules_to_run:
    logger.info(f"Initializing module: {module.__name__}")
    module.run(*args)

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
