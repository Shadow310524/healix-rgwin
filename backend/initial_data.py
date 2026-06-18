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

    # 3. Products to seed
    products_data = [
        { 
            "name": "Dienowin 2mg", 
            "category_name": "Hormone Therapy", 
            "price": "Enquire", 
            "description": "(Dienogest 2 mg) Highly effective targeted therapy for endometriosis and hormonal balance.", 
            "benefits": ["Effective management of endometriosis", "Hormonal regulation", "Reduces pelvic pain"], 
            "ingredients": ["Dienogest 2 mg"], 
            "image_url": "assets/images/products/dienowin.png" 
        },
        { 
            "name": "Flora-Gem", 
            "category_name": "Vaginal Health", 
            "price": "Enquire", 
            "description": "Advanced probiotic formula for optimal vaginal flora and pH balance.", 
            "benefits": ["Maintains healthy vaginal pH", "Prevents recurring infections", "Supports natural microbiome"], 
            "ingredients": ["Lactobacillus crispatus", "Lactobacillus rhamnosus"], 
            "image_url": "assets/images/products/flora-gem.png" 
        },
        { 
            "name": "Labemax 100", 
            "category_name": "Cardiovascular", 
            "price": "Enquire", 
            "benefits": "Manages high blood pressure, Safe during pregnancy, Dual alpha and beta-blocker action", 
            "ingredients": "Labetalol 100mg", 
            "image_url": "https://images.unsplash.com/photo-1550572017-edcfbfc9cb9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
        }
    ]

    for p in products_data:
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
