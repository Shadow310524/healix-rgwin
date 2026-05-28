from typing import Any, List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.core.logging_config import get_logger
from app.services.email_service import send_enquiry_email

logger = get_logger("healix.enquiries")

router = APIRouter()

@router.get("/", response_model=List[schemas.Enquiry])
def read_enquiries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    enquiries = crud.get_enquiries(db, skip=skip, limit=limit)
    logger.info(f"Enquiries listed | Count: {len(enquiries)} | By: {current_user.email}")
    return enquiries

@router.post("/", response_model=schemas.Enquiry)
def create_enquiry(
    *,
    db: Session = Depends(deps.get_db),
    enquiry_in: schemas.EnquiryCreate,
    background_tasks: BackgroundTasks,
) -> Any:
    enquiry = crud.create_enquiry(db=db, enquiry=enquiry_in)
    logger.info(f"Enquiry CREATED | ID: {enquiry.id} | Name: '{enquiry_in.name}' | Email: '{enquiry_in.email}'")
    
    # Extract optional fields safely using getattr in case they don't exist in older schemas
    phone = getattr(enquiry_in, 'phone', None)
    product_name = getattr(enquiry_in, 'product_name', None)
    
    background_tasks.add_task(
        send_enquiry_email,
        name=enquiry_in.name,
        email=enquiry_in.email,
        message=enquiry_in.message,
        phone=phone,
        product_name=product_name
    )
    
    return enquiry
