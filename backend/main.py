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
    Structured Logging & Correlation ID middleware.
    Tracks Correlation ID, HTTP Method, Endpoint, Status Code, IP Address, Duration, User ID.
    Never exposes internal details or stack traces to clients.
    """
    import uuid
    import time
    from jose import jwt as jose_jwt
    from app.crud import log_audit_event
    
    start_time = time.time()
    
    # 1. Correlation ID
    correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    
    # 2. Extract user metadata silently from token
    user_email = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jose_jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")
            if user_id:
                user_email = f"User#{user_id}"
        except Exception:
            pass
            
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        
        # Inject correlation ID in response headers
        response.headers["X-Request-ID"] = correlation_id
        
        # Structured log output
        logger.info(
            f"REQ | ID: {correlation_id} | IP: {client_ip} | User: {user_email or 'Anonymous'} | "
            f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)"
        )
        return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        
        # Server-side structured error log with trace
        logger.error(
            f"ERROR | ID: {correlation_id} | IP: {client_ip} | User: {user_email or 'Anonymous'} | "
            f"{request.method} {request.url.path} -> 500 UNHANDLED EXCEPTION ({duration_ms:.1f}ms) | "
            f"Details: {str(e)}\n{traceback.format_exc()}"
        )
        
        # Persistent Audit Logging for Critical Failures
        try:
            with SessionLocal() as db:
                log_audit_event(
                    db,
                    user_email or "System",
                    "Error",
                    f"{request.method} {request.url.path}",
                    "Failure",
                    client_ip,
                    correlation_id
                )
        except Exception as audit_err:
            logger.error(f"Audit log failed during 500 error: {audit_err}")
            
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An unexpected error occurred on the server.",
                "request_id": correlation_id
            }
        )


# ── Application Lifecycle ─────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Healix Backend Server STARTED")
    logger.info(f"Project: {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Debug Mode: {settings.DEBUG_MODE}")
    logger.info("=" * 60)
    
    # ── Startup Configuration Validation ──
    logger.info("Validating configuration settings...")
    if settings.SECRET_KEY == "DEVELOPMENT_SECRET_KEY_DONT_USE_IN_PROD" and not settings.DEBUG_MODE:
        logger.critical("CRITICAL: SECRET_KEY is set to default fallback in production mode!")
        raise RuntimeError("Production SECRET_KEY must be configured!")
        
    if not settings.DATABASE_URL:
        logger.critical("CRITICAL: DATABASE_URL is missing!")
        raise RuntimeError("DATABASE_URL must be configured!")
        
    if not settings.GEMINI_API_KEY:
        logger.warning("WARNING: GEMINI_API_KEY is missing! RAG AI chatbot will fail.")
        
    if not settings.CLOUDINARY_CLOUD_NAME or not settings.CLOUDINARY_API_KEY:
        logger.warning("WARNING: Cloudinary is not configured! PDF and image uploads will fail.")
        
    logger.info("Configuration validation completed successfully.")


# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to the Healix API", "version": settings.VERSION}


# ── Health & Readiness Endpoints ──────────────────────────────────────────────
@app.get("/health", tags=["Infrastructure"])
def health_check():
    """
    Liveness probe — confirms the server process is alive and returns status.
    """
    db_status = "connected"
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"
        
    import datetime
    return {
        "status": "ok",
        "database": db_status,
        "version": settings.VERSION,
        "server_time": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }


@app.get("/ready", tags=["Infrastructure"])
def readiness_check():
    """
    Readiness probe — verifies all external configurations and database connections.
    """
    checks = {
        "database": "unreachable",
        "gemini": "misconfigured",
        "cloudinary": "misconfigured",
        "environment_variables": "missing"
    }
    status_code = 200
    
    # 1. Database Check
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        checks["database"] = "connected"
    except Exception as e:
        logger.error(f"Readiness DB probe failed: {e}")
        status_code = 503
        
    # 2. Gemini Check
    if settings.GEMINI_API_KEY:
        checks["gemini"] = "configured"
    else:
        status_code = 503
        
    # 3. Cloudinary Check
    if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY:
        checks["cloudinary"] = "configured"
    else:
        status_code = 503
        
    # 4. Env Configuration Check
    if settings.SECRET_KEY and settings.SECRET_KEY != "DEVELOPMENT_SECRET_KEY_DONT_USE_IN_PROD":
        checks["environment_variables"] = "configured"
    else:
        checks["environment_variables"] = "development_fallback"
        
    response_data = {
        "status": "ready" if status_code == 200 else "not_ready",
        "checks": checks
    }
    
    if status_code != 200:
        return JSONResponse(status_code=status_code, content=response_data)
    return response_data
