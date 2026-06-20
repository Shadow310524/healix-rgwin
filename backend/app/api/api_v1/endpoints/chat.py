from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from typing import List
import google.generativeai as genai
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api import deps
from app.services.rag_service import retrieve_relevant_chunks
from app.core.system_prompts import RAG_CHATBOT_SYSTEM_PROMPT
from app.core.logging_config import get_logger

logger = get_logger("healix.chat")

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# Maximum characters allowed in a single user message
MAX_MESSAGE_LENGTH = 2000


class ChatMessage(BaseModel):
    role: str
    content: str

    @validator("content")
    def content_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()

    @validator("role")
    def role_must_be_valid(cls, v):
        if v not in ("user", "assistant", "model"):
            raise ValueError("Role must be 'user' or 'assistant'")
        return v


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str


def _sanitize_user_input(text: str) -> str:
    """
    SECURITY: Sanitize user input before injecting into the prompt.
    Strips prompt injection markers and limits length.
    """
    # Truncate to prevent token abuse
    text = text[:MAX_MESSAGE_LENGTH]
    # Strip common prompt injection patterns
    injection_patterns = [
        "ignore previous instructions",
        "ignore all previous",
        "disregard your instructions",
        "you are now",
        "forget your system prompt",
        "new instruction:",
        "system:",
        "</system>",
        "<system>",
    ]
    lower_text = text.lower()
    for pattern in injection_patterns:
        if pattern in lower_text:
            logger.warning(f"Potential prompt injection attempt detected. Pattern: '{pattern}'")
            # Don't block the user but sanitize the dangerous fragment
            # Replace only the matched part in a case-insensitive way
            import re
            text = re.sub(re.escape(pattern), "[removed]", text, flags=re.IGNORECASE)
    return text


@router.post("/", response_model=ChatResponse)
@limiter.limit("20/minute")  # SECURITY: Prevent AI cost abuse
def chat_with_bot(
    request: Request,
    chat_request: ChatRequest,
    db: Session = Depends(deps.get_db),
):
    """
    AI Clinical Assistant endpoint.

    Security hardening applied:
    - Rate limited: 20 requests/minute per IP
    - Input sanitized against prompt injection patterns
    - User input is isolated in a bracketed block (never merged with system instructions)
    - Graceful fallback if Gemini is unavailable
    - Raw errors are never exposed to the client
    """
    latest_query = None
    try:
        # 1. Extract the latest user query
        user_messages = [m for m in chat_request.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message provided")

        raw_query = user_messages[-1].content

        # 2. SECURITY: Sanitize input before any prompt construction
        latest_query = _sanitize_user_input(raw_query)

        logger.info(f"Chat request | Length: {len(latest_query)} chars")

        # 3. Retrieve relevant semantic chunks from DB
        try:
            relevant_chunks = retrieve_relevant_chunks(db, latest_query, top_k=3)
            logger.info(f"RAG retrieved {len(relevant_chunks)} chunks")
        except Exception as rag_err:
            logger.error(f"RAG retrieval failed: {rag_err}", exc_info=True)
            relevant_chunks = []

        # 4. Format the context
        context_text = "\n\n".join([f"- {chunk['text']}" for chunk in relevant_chunks])
        if not context_text:
            context_text = "No relevant product information found in the database."

        # 5. Build the system instruction
        system_instruction = RAG_CHATBOT_SYSTEM_PROMPT.format(context=context_text)

        # 6. Format conversation history (safe, excluding latest query)
        formatted_history = []
        for msg in chat_request.messages[:-1]:
            role = "user" if msg.role == "user" else "model"
            if not formatted_history and role == "model":
                continue
            formatted_history.append({"role": role, "parts": [msg.content]})

        # 7. SECURITY: User input is ISOLATED in a clearly delimited block.
        # This prevents the user's text from overriding system instructions.
        final_prompt = (
            f"SYSTEM INSTRUCTIONS:\n{system_instruction}\n\n"
            f"---USER QUESTION BEGIN---\n{latest_query}\n---USER QUESTION END---"
        )

        # 8. Call Gemini with graceful fallback
        try:
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            chat = model.start_chat(history=formatted_history)
            response = chat.send_message(final_prompt)
            reply_text = response.text
            logger.info(f"Chat response sent | Length: {len(reply_text)} chars")
        except Exception as gemini_err:
            # SECURITY: Never expose Gemini SDK errors to the client.
            # Graceful fallback instead of a raw 500 error.
            logger.error(f"Gemini API call failed: {gemini_err}", exc_info=True)
            reply_text = (
                "Our clinical assistant is temporarily unavailable. "
                "Please try again in a moment, or use the Enquire Now button "
                "to contact our support team directly."
            )

        return ChatResponse(reply=reply_text)

    except HTTPException:
        raise
    except Exception as e:
        # SECURITY: Generic error — never expose internal details.
        logger.error(
            f"Chat CRASH | Query: '{str(latest_query)[:50]}' | Error: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again.",
        )
