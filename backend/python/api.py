from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from utils.logger import get_logger
from middleware import metrics_middleware
from utils.connection_manager import kill_all_connections

from routes.root import router as root_router
from routes.metrics import router as metrics_router
from routes.jobs import router as jobs_router
from routes.signup import router as signup_router
from routes.send_email import router as send_email_router
from routes.database import router as database_router
from routes.login import router as login_router
from routes.geo import router as router_geo
from routes.chat import chat_router

import time
logger = get_logger(__name__)

app = FastAPI(
    title="JobSearch API",
    description="API for job search and recruitment operations",
    version="1.0.0",
    websocket_ping_interval=20.0,  # Send ping every 20 seconds
    websocket_ping_timeout=20.0,   # Wait 20 seconds for pong response
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"]   # Allows all headers
)
app.add_middleware(SessionMiddleware,secret_key="your_secret_key")

# Add metrics middleware
app.middleware("http")(metrics_middleware)

# Include routers from other modules
app.include_router(root_router)
app.include_router(metrics_router)
app.include_router(jobs_router)
app.include_router(signup_router)
app.include_router(send_email_router)
app.include_router(login_router)
app.include_router(router_geo)
app.include_router(chat_router)
app.include_router(database_router)


if __name__ == "__main__":
    import uvicorn
    logger.info("Cleaning up existing database connections...")
    kill_all_connections()
    logger.info("Starting the application")
    time.sleep(3)
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=10000,
        reload=True
    )