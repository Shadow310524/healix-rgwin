import sys
from app.db.session import SessionLocal
from app import crud, schemas
from app.core.config import settings

def init_db(db: SessionLocal) -> None:
    # 1. Create Superuser
    user = crud.get_user_by_email(db, email="admin@healixtest.com")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@healixtest.com",
            password="admin123",
            is_superuser=True,
        )
        user = crud.create_user(db, user=user_in)
        print("Superuser created")
    else:
        print("Superuser already exists")

    # 2. Create Categories
    categories_to_create = ["Hormone Therapy", "Supplements", "Vaginal Health", "Cardiovascular"]
    db_categories = {}
    for cat_name in categories_to_create:
        existing = db.query(crud.category_model.Category).filter(crud.category_model.Category.name == cat_name).first()
        if not existing:
            cat_in = schemas.CategoryCreate(name=cat_name)
            existing = crud.create_category(db, category=cat_in)
            print(f"Category '{cat_name}' created")
        db_categories[cat_name] = existing.id

    # 3. Create Products
    products_to_create = [
        { 
            "name": "Dienowin 2mg", 
            "category_name": "Hormone Therapy", 
            "price": "Enquire", 
            "description": "(Dienogest 2 mg) Highly effective targeted therapy for endometriosis and hormonal balance.", 
            "benefits": "Effective management of endometriosis, Hormonal regulation, Reduces pelvic pain", 
            "ingredients": "Dienogest 2 mg", 
            "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
        },
        { 
            "name": "Lrgwin SYRUP", 
            "category_name": "Supplements", 
            "price": "Enquire", 
            "description": "Each 15 ml contain L-Arginine HCL - 3 gram (225 ml). Premium syrup formulated to support cardiovascular health and blood flow.", 
            "benefits": "Supports cardiovascular health, Improves blood circulation, Aids in prenatal care", 
            "ingredients": "L-Arginine HCL (3g per 15ml)", 
            "image_url": "https://images.unsplash.com/photo-1550572017-edcfbfc9cb9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
        },
        { 
            "name": "Norwin CR", 
            "category_name": "Hormone Therapy", 
            "price": "Enquire", 
            "description": "(Northisterone 10mg) Controlled release formulation for cycle regulation and management of heavy menstrual bleeding.", 
            "benefits": "Regulates menstrual cycles, Manages heavy bleeding, Controlled release for steady absorption", 
            "ingredients": "Northisterone 10mg", 
            "image_url": "https://images.unsplash.com/photo-1628771065518-0d82f1938462?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
        },
        { 
            "name": "Flora-gem", 
            "category_name": "Vaginal Health", 
            "price": "Enquire", 
            "description": "Vaginal Infection Veg capsules designed to restore healthy flora and treat common vaginal infections naturally.", 
            "benefits": "Treats vaginal infections, Restores natural pH balance, 100% Vegetarian capsules", 
            "ingredients": "Probiotic blend, Natural botanical extracts", 
            "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
        },
        { 
            "name": "Labemax 100mg", 
            "category_name": "Cardiovascular", 
            "price": "Enquire", 
            "description": "(Labetalol 100mg) Specialized medication for the management of hypertension, particularly useful in pregnancy-induced hypertension.", 
            "benefits": "Manages high blood pressure, Safe during pregnancy, Dual alpha and beta-blocker action", 
            "ingredients": "Labetalol 100mg", 
            "image_url": "https://images.unsplash.com/photo-1550572017-edcfbfc9cb9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
        }
    ]

    for p in products_to_create:
        existing = db.query(crud.product_model.Product).filter(crud.product_model.Product.name == p["name"]).first()
        if not existing:
            cat_id = db_categories.get(p["category_name"])
            p_in = schemas.ProductCreate(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                benefits=p["benefits"],
                ingredients=p["ingredients"],
                image_url=p["image_url"],
                category_id=cat_id
            )
            crud.create_product(db, product=p_in)
            print(f"Product '{p['name']}' created")

def main() -> None:
    print("Creating initial data")
    db = SessionLocal()
    init_db(db)
    print("Initial data created")

if __name__ == "__main__":
    main()
