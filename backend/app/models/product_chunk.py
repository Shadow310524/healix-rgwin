from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.session import Base

class ProductChunk(Base):
    __tablename__ = "product_chunks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    chunk_text = Column(Text, nullable=False)
    
    # We use a standard Postgres ARRAY of Floats to store the vector embeddings
    # This avoids needing the pgvector extension for simple use cases.
    embedding = Column(ARRAY(Float), nullable=False)
    
    product = relationship("Product", backref="chunks")
