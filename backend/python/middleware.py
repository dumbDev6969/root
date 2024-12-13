from fastapi import Request
from starlette.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import time
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize Prometheus metrics
if 'request_count' not in REGISTRY._names_to_collectors:
    REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])
    REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])
    ACTIVE_REQUESTS = Gauge('active_requests', 'Active requests')
else:
    REQUEST_COUNT = REGISTRY._names_to_collectors['request_count']
    REQUEST_LATENCY = REGISTRY._names_to_collectors['request_latency_seconds']
    ACTIVE_REQUESTS = REGISTRY._names_to_collectors['active_requests']

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

async def metrics():
    logger.info("Metrics endpoint accessed")
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
