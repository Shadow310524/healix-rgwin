from sqlalchemy.orm import Session
from app.models import user as user_model, product as product_model, category as category_model, enquiry as enquiry_model
from app.schemas import user as user_schema, product as product_schema, category as category_schema, enquiry as enquiry_schema
from app.core.security import get_password_hash

# User CRUD
def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password, is_superuser=user.is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Category CRUD
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(category_model.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: category_schema.CategoryCreate):
    db_category = category_model.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Product CRUD
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(product_model.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: product_schema.ProductCreate):
    db_product = product_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: product_schema.ProductUpdate):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == product_id).first()
    if not db_product:
        return None
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == product_id).first()
    if not db_product:
        return None
        
    # Eagerly load category to prevent DetachedInstanceError when FastAPI serializes the response
    _ = db_product.category
        
    # Prevent RAG hallucination by deleting all text chunks associated with this product
    from app.models.product_chunk import ProductChunk
    db.query(ProductChunk).filter(ProductChunk.product_id == product_id).delete()
    
    db.delete(db_product)
    db.commit()
    return db_product

# Enquiry CRUD
def get_enquiries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(enquiry_model.Enquiry).order_by(enquiry_model.Enquiry.created_at.desc()).offset(skip).limit(limit).all()

def create_enquiry(db: Session, enquiry: enquiry_schema.EnquiryCreate):
    db_enquiry = enquiry_model.Enquiry(**enquiry.model_dump())
    db.add(db_enquiry)
    db.commit()
    db.refresh(db_enquiry)
    return db_enquiry
