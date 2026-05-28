from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.core.logging_config import get_logger

logger = get_logger("healix.categories")

router = APIRouter()

@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    categories = crud.get_categories(db, skip=skip, limit=limit)
    logger.info(f"Categories listed | Count: {len(categories)}")
    return categories

@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    category = crud.create_category(db=db, category=category_in)
    logger.info(f"Category CREATED | ID: {category.id} | Name: '{category.name}' | By: {current_user.email}")
    return category
