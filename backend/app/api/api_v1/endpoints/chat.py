from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

from app.api import deps
from app.services.rag_service import retrieve_relevant_chunks
from app.core.system_prompts import RAG_CHATBOT_SYSTEM_PROMPT

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    db: Session = Depends(deps.get_db)
):
    try:
        # 1. Get the latest user query
        user_messages = [m for m in request.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message provided")
        latest_query = user_messages[-1].content

        # 2. Retrieve relevant semantic chunks from DB
        relevant_chunks = retrieve_relevant_chunks(db, latest_query, top_k=3)
        
        # 3. Format the context
        context_text = "\n\n".join([f"- {chunk['text']}" for chunk in relevant_chunks])
        if not context_text:
            context_text = "No relevant product information found in the database."

        # 4. Prepare the prompt for Gemini
        system_instruction = RAG_CHATBOT_SYSTEM_PROMPT.format(context=context_text)
        
        # Format history for Gemini
        formatted_history = []
        for msg in request.messages[:-1]:  # Exclude the latest query
            role = "user" if msg.role == "user" else "model"
            # Gemini requires conversation to start with 'user'. Skip leading 'model' messages.
            if not formatted_history and role == "model":
                continue
            formatted_history.append({"role": role, "parts": [msg.content]})

        # 5. Call Gemini Chat Model
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(latest_query)
        
        return ChatResponse(reply=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
