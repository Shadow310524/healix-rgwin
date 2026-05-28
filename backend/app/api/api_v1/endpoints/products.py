from typing import Any, List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.services.rag_service import process_product_for_rag
from app.core.logging_config import get_logger

logger = get_logger("healix.products")

router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    products = crud.get_products(db, skip=skip, limit=limit)
    logger.info(f"Products listed | Count: {len(products)}")
    return products

@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.create_product(db=db, product=product_in)
    
    # Process the product in the background for RAG embeddings
    background_tasks.add_task(process_product_for_rag, db, product)
    
    logger.info(f"Product CREATED | ID: {product.id} | Name: '{product.name}' | By: {current_user.email}")
    return product
