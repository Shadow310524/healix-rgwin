from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(String, nullable=True)
    mrp = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    benefits = Column(JSON, nullable=True) 
    ingredients = Column(JSON, nullable=True)
    
    # Audit trail & recovery: soft delete indicator
    is_deleted = Column(Boolean, default=False, index=True, nullable=False)
    
    # Concurrency control: Optimistic locking version
    version_id = Column(Integer, default=1, nullable=False)
    
    # Index added for performance joins
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    category = relationship("Category", back_populates="products")

    __mapper_args__ = {
        "version_id_col": version_id
    }
