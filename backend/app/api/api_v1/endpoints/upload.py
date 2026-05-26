from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.api import deps
from app.core.config import settings
from app import models
import cloudinary
import cloudinary.uploader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read file content
        contents = await file.read()
        
        logger.info(f"Attempting to upload file to Cloudinary: {file.filename}")
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            contents,
            folder="healix_products",
            resource_type="image"
        )
        
        logger.info(f"Cloudinary upload successful: {result.get('secure_url')}")
        return {"url": result.get("secure_url")}
    except Exception as e:
        logger.error(f"Cloudinary upload error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
