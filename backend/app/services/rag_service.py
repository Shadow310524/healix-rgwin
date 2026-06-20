import google.generativeai as genai
import numpy as np
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_chunk import ProductChunk
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Using the standard embedding model supported by the current SDK
EMBEDDING_MODEL = "models/gemini-embedding-001"

def get_embedding(text: str) -> list[float]:
    """Generates a vector embedding for a given text string."""
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

def get_query_embedding(text: str) -> list[float]:
    """Generates an embedding optimized for a search query."""
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        return []

def chunk_text(text: str, max_words: int = 50) -> list[str]:
    """Splits text into smaller semantic chunks (sentences)."""
    if not text:
        return []
    
    # Simple semantic chunking by sentences for now
    sentences = [s.strip() + "." for s in text.replace('!', '.').replace('?', '.').split('.') if len(s.strip()) > 5]
    
    chunks = []
    current_chunk = []
    current_words = 0
    
    for sentence in sentences:
        words = len(sentence.split())
        if current_words + words > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_words = words
        else:
            current_chunk.append(sentence)
            current_words += words
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

from app.db.session import SessionLocal

def process_product_for_rag(product_id: int):
    """Chunks product details, gets embeddings, and saves to DB."""
    
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return
            
        # First, delete any existing chunks for this product to prevent duplication
        delete_product_from_rag(product_id)
        
        # Build a comprehensive text representation of the product
        full_text = f"Product Name: {product.name}. "
        if product.description:
            full_text += f"Description: {product.description}. "
        if product.benefits:
            full_text += f"Benefits: {product.benefits}. "
        if product.ingredients:
            full_text += f"Ingredients: {product.ingredients}. "
            
        # Chunk the text
        chunks = chunk_text(full_text)
        
        # Create DB records
        for chunk in chunks:
            embedding = get_embedding(chunk)
            if embedding:
                db_chunk = ProductChunk(
                    product_id=product.id,
                    chunk_text=chunk,
                    embedding=embedding
                )
                db.add(db_chunk)
                
        db.commit()

def delete_product_from_rag(product_id: int):
    """Deletes all RAG chunks associated with a specific product ID."""
    with SessionLocal() as db:
        try:
            db.query(ProductChunk).filter(ProductChunk.product_id == product_id).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error deleting chunks for product {product_id}: {e}")

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Calculates cosine similarity between two vectors."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_relevant_chunks(db: Session, query: str, top_k: int = 3) -> list[dict]:
    """Finds the most relevant product chunks for a given query."""
    query_vector = get_query_embedding(query)
    if not query_vector:
        return []
        
    # Convert query vector list to postgres vector string representation e.g. '[0.1,0.2,...]'
    vector_str = "[" + ",".join(map(str, query_vector)) + "]"
    
    # Performance Optimization: query pgvector directly inside database using <=> cosine distance.
    # We use CAST(:query_vector AS vector) to prevent double-colon compilation errors in SQLAlchemy.
    from sqlalchemy import text
    sql = text("""
        SELECT product_id, chunk_text, 1 - (embedding <=> CAST(:query_vector AS vector)) AS similarity
        FROM product_chunks
        ORDER BY embedding <=> CAST(:query_vector AS vector)
        LIMIT :top_k;
    """)
    
    try:
        query_results = db.execute(sql, {"query_vector": vector_str, "top_k": top_k}).fetchall()
        
        # Phase 1 Optimization: Discard chunks that are below similarity cutoff threshold
        filtered_results = [
            {
                "product_id": row[0],
                "text": row[1],
                "similarity": float(row[2])
            }
            for row in query_results
            if float(row[2]) >= settings.RAG_SIMILARITY_THRESHOLD
        ]
        return filtered_results
    except Exception as e:
        print(f"Error retrieving relevant chunks: {e}")
        return []
