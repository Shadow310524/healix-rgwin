from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.core.logging_config import get_logger

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
) -> Any:
    enquiry = crud.create_enquiry(db=db, enquiry=enquiry_in)
    logger.info(f"Enquiry CREATED | ID: {enquiry.id} | Name: '{enquiry_in.name}' | Email: '{enquiry_in.email}'")
    return enquiry
