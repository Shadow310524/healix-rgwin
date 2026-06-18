import google.generativeai as genai
import numpy as np
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_chunk import ProductChunk
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Using the standard embedding model supported by the current SDK
EMBEDDING_MODEL = "models/text-embedding-004"

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

def process_product_for_rag(db: Session, product: Product):
    """Chunks product details, gets embeddings, and saves to DB."""
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
        
    # Get all chunks from DB
    all_chunks = db.query(ProductChunk).all()
    
    results = []
    for chunk in all_chunks:
        sim = cosine_similarity(query_vector, chunk.embedding)
        results.append({
            "product_id": chunk.product_id,
            "text": chunk.chunk_text,
            "similarity": float(sim)
        })
        
    # Sort by highest similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Return top K results
    return results[:top_k]
