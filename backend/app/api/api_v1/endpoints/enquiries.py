from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Enquiry])
def read_enquiries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    enquiries = crud.get_enquiries(db, skip=skip, limit=limit)
    return enquiries

@router.post("/", response_model=schemas.Enquiry)
def create_enquiry(
    *,
    db: Session = Depends(deps.get_db),
    enquiry_in: schemas.EnquiryCreate,
) -> Any:
    enquiry = crud.create_enquiry(db=db, enquiry=enquiry_in)
    return enquiry
