from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from utils.logger import get_logger
from middleware import metrics_middleware
from routes.root import router as root_router
from routes.metrics import router as metrics_router
from routes.jobs import router as jobs_router
from routes.signup import router as signup_router
from routes.send_email import router as send_email_router
from routes.query_and_delete import router as query_and_delete_router
from routes.update import router as update_router
from routes.database import router as database_router

logger = get_logger(__name__)

app = FastAPI(
    title="JobSearch API",
    description="API for job search and recruitment operations",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
# app.include_router(query_and_delete_router)
# app.include_router(update_router)
app.include_router(database_router)
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the application")
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=11352,
        reload=True
    )
