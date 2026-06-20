from typing import Any, List
from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.services.rag_service import process_product_for_rag, delete_product_from_rag
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

@router.get("/{id}", response_model=schemas.Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    from fastapi import HTTPException
    from sqlalchemy import text
    
    product = db.query(models.Product).filter(models.Product.id == id, models.Product.is_deleted == False).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Analytics View Counter: Increment views on detail access
    try:
        db.execute(
            text("UPDATE products SET views = views + 1 WHERE id = :id"),
            {"id": id}
        )
        db.commit()
        db.refresh(product)
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to increment views for product {id}: {e}")
        
    return product

@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    product = crud.create_product(db=db, product=product_in)
    
    # Process the product in the background for RAG embeddings
    background_tasks.add_task(process_product_for_rag, product.id)
    
    logger.info(f"Product CREATED | ID: {product.id} | Name: '{product.name}' | By: {current_user.email}")
    crud.log_audit_event(
        db, 
        current_user.email, 
        "Product Created", 
        f"Product ID: {product.id} | Name: '{product.name}'", 
        "Success", 
        request.client.host,
        getattr(request.state, "correlation_id", None)
    )
    return product

@router.put("/{id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    product_in: schemas.ProductUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    from fastapi import HTTPException
    product = crud.update_product(db=db, product_id=id, product=product_in)
    if not product:
        crud.log_audit_event(
            db, 
            current_user.email, 
            "Product Updated", 
            f"Product ID: {id}", 
            "Failure", 
            request.client.host,
            getattr(request.state, "correlation_id", None)
        )
        raise HTTPException(status_code=404, detail="Product not found")
    
    background_tasks.add_task(process_product_for_rag, product.id)
    
    logger.info(f"Product UPDATED | ID: {product.id} | Name: '{product.name}' | By: {current_user.email}")
    crud.log_audit_event(
        db, 
        current_user.email, 
        "Product Updated", 
        f"Product ID: {product.id} | Name: '{product.name}'", 
        "Success", 
        request.client.host,
        getattr(request.state, "correlation_id", None)
    )
    return product

@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    from fastapi import HTTPException
    product = crud.delete_product(db=db, product_id=id)
    if not product:
        crud.log_audit_event(
            db, 
            current_user.email, 
            "Product Deleted", 
            f"Product ID: {id}", 
            "Failure", 
            request.client.host,
            getattr(request.state, "correlation_id", None)
        )
        raise HTTPException(status_code=404, detail="Product not found")
    
    background_tasks.add_task(delete_product_from_rag, id)
    
    logger.info(f"Product DELETED | ID: {product.id} | Name: '{product.name}' | By: {current_user.email}")
    crud.log_audit_event(
        db, 
        current_user.email, 
        "Product Deleted", 
        f"Product ID: {product.id} | Name: '{product.name}'", 
        "Success", 
        request.client.host,
        getattr(request.state, "correlation_id", None)
    )
    return product
