from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from app.api import deps
from app.core.config import settings
from app.core.logging_config import get_logger
from app import models
import cloudinary
import cloudinary.uploader

logger = get_logger("healix.upload")

router = APIRouter()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Upload an image to Cloudinary and return the URL.
    Uses run_in_threadpool to prevent blocking the event loop
    while waiting for Cloudinary's synchronous upload.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read file content (async-safe)
        contents = await file.read()
        
        logger.info(f"Upload started | File: {file.filename} | Size: {len(contents)} bytes | User: {current_user.email}")
        
        # Run synchronous Cloudinary upload in a threadpool to avoid blocking
        result = await run_in_threadpool(
            cloudinary.uploader.upload,
            contents,
            folder="healix_products",
            resource_type="image"
        )
        
        url = result.get("secure_url")
        logger.info(f"Upload successful | File: {file.filename} | URL: {url}")
        return {"url": url}
    except Exception as e:
        logger.error(f"Upload failed | File: {file.filename} | Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
