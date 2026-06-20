import time
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
from app.db.session import SessionLocal

# Initialize logging FIRST, before anything else
setup_logging()
logger = get_logger("healix.main")

# ── Rate Limiter ──────────────────────────────────────────────────────────────
# Uses in-memory storage by default (no Redis required).
# Safe to deploy immediately on the existing server.
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # Hide docs in production to reduce attack surface
    docs_url="/docs" if settings.DEBUG_MODE else None,
    redoc_url="/redoc" if settings.DEBUG_MODE else None,
)

# Attach rate limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ──────────────────────────────────────────────────────────────────────
# SECURITY FIX: Replaced wildcard `allow_origins=["*"]` with a strict list.
# Add your Vercel production URL and any local dev origins here.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# ── Secure Response Headers Middleware ────────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Injects security headers on every response.
    Protects against clickjacking, MIME sniffing, and XSS.
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    # Remove server fingerprint header (MutableHeaders uses del, not .pop())
    try:
        del response.headers["server"]
    except KeyError:
        pass
    return response


# ── Request Logging Middleware ────────────────────────────────────────────────
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Middleware that logs every incoming HTTP request with:
    - Method (GET, POST, etc.)
    - Path (/api/v1/products/)
    - Status Code (200, 404, 500, etc.)
    - Time taken in milliseconds
    NOTE: Sensitive headers (Authorization) are intentionally NOT logged.
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
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred. Please try again."},
        )


# ── Application Lifecycle ─────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Healix Backend Server STARTED")
    logger.info(f"Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Debug Mode: {settings.DEBUG_MODE}")
    logger.info("=" * 60)


# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to the Healix API", "version": settings.VERSION}


# ── Health & Readiness Endpoints ──────────────────────────────────────────────
@app.get("/health", tags=["Infrastructure"])
def health_check():
    """
    Liveness probe — confirms the server process is alive.
    Used by load balancers and container orchestrators (Kubernetes, Railway, Render).
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


@app.get("/readiness", tags=["Infrastructure"])
def readiness_check():
    """
    Readiness probe — confirms the server AND its database connection are ready.
    If the DB is unreachable, returns 503 so the load balancer stops routing traffic here.
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # SQLAlchemy 2.0 requires text() wrapper
        db.close()
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error(f"Readiness check FAILED: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "database": "unreachable"},
        )
