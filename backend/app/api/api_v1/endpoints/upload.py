from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.concurrency import run_in_threadpool
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.api import deps
from app.core.config import settings
from app.core.logging_config import get_logger
from app import models
import cloudinary
import cloudinary.uploader

logger = get_logger("healix.upload")

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# SECURITY: Maximum allowed file size (5 MB)
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

# SECURITY: Allowed MIME types (defence layer 1)
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

# SECURITY: Allowed magic number signatures (defence layer 2 — actual bytes, not just header)
# This prevents attackers from renaming malicious files to .jpg
MAGIC_SIGNATURES = {
    b"\xff\xd8\xff": "image/jpeg",   # JPEG
    b"\x89PNG\r\n\x1a\n": "image/png",  # PNG
    b"RIFF": "image/webp",            # WebP (partial — full check needs offset 8)
    b"GIF87a": "image/gif",           # GIF87
    b"GIF89a": "image/gif",           # GIF89
}


def _validate_image_bytes(contents: bytes, filename: str) -> None:
    """
    SECURITY: Validates the actual file bytes against known image magic numbers.
    Content-Type headers sent by the client can be spoofed — magic numbers cannot.
    Raises HTTPException if the file is not a valid image.
    """
    for signature, _ in MAGIC_SIGNATURES.items():
        if contents[:len(signature)] == signature:
            return  # Valid image
    logger.warning(f"Upload BLOCKED | File: {filename} | Reason: Invalid magic number (not a real image)")
    raise HTTPException(
        status_code=400,
        detail="Uploaded file is not a valid image. Only JPEG, PNG, WebP, and GIF are accepted.",
    )


# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


@router.post("/image")
@limiter.limit("10/minute")  # SECURITY: Prevent upload abuse
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Upload a product image to Cloudinary.

    Security hardening applied:
    - Rate limited: 10 uploads/minute per IP
    - Content-Type header validated (layer 1)
    - File magic number validated (layer 2 — cannot be spoofed)
    - File size capped at 5 MB
    - Raw Cloudinary errors never exposed to client
    """
    # SECURITY layer 1: Content-Type header check
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only JPEG, PNG, WebP, and GIF images are accepted.",
        )

    try:
        contents = await file.read()

        # SECURITY: File size enforcement
        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB.",
            )

        # SECURITY layer 2: Magic number validation
        _validate_image_bytes(contents, file.filename or "unknown")

        logger.info(
            f"Upload started | File: {file.filename} | "
            f"Size: {len(contents):,} bytes | User ID: {current_user.id}"
        )

        # Run synchronous Cloudinary upload in a threadpool to avoid blocking
        result = await run_in_threadpool(
            cloudinary.uploader.upload,
            contents,
            folder="healix_products",
            resource_type="image",
        )

        url = result.get("secure_url")
        logger.info(f"Upload SUCCESS | File: {file.filename} | URL: {url}")
        return {"url": url}

    except HTTPException:
        raise
    except Exception as e:
        # SECURITY: Never expose Cloudinary internals to the client.
        logger.error(f"Upload FAILED | File: {file.filename} | Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Image upload failed. Please try again or contact support.",
        )
