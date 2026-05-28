import time
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger

# Initialize logging FIRST, before anything else
setup_logging()
logger = get_logger("healix.main")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins so Vercel can connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Middleware that logs every incoming HTTP request with:
    - Method (GET, POST, etc.)
    - Path (/api/v1/products/)
    - Status Code (200, 404, 500, etc.)
    - Time taken in milliseconds
    """
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.0f}ms)"
        )
        return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            f"{request.method} {request.url.path} -> 500 UNHANDLED ERROR ({duration_ms:.0f}ms)\n"
            f"{traceback.format_exc()}"
        )
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Healix Backend Server STARTED")
    logger.info(f"Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info("=" * 60)


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to the Healix API"}
