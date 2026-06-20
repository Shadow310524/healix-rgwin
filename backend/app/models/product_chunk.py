from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.session import Base

class ProductChunk(Base):
    __tablename__ = "product_chunks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    chunk_text = Column(Text, nullable=False)
    
    # RAG OPTIMIZATION: Stores vector embeddings natively as pgvector type.
    # Dimensions: 3072 matching models/gemini-embedding-001 output.
    embedding = Column(Vector(3072), nullable=False)
    
    product = relationship("Product", backref="chunks")
