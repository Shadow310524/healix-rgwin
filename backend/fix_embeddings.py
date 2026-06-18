import asyncio
from app.db.session import SessionLocal
from app.models.product import Product
from app.services.rag_service import index_product

async def main():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print(f"Found {len(products)} products to index...")
        for p in products:
            print(f"Indexing: {p.name}")
            try:
                index_product(p.id, p.name, p.description, p.benefits, p.ingredients)
                print(f"✅ Success: {p.name}")
            except Exception as e:
                print(f"❌ Failed: {p.name} - {str(e)}")
        print("Done!")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
