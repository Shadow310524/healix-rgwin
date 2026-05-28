from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger("healix.auth")

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        user = crud.get_user_by_email(db, email=form_data.username)
        if not user or not security.verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Login FAILED | Email: '{form_data.username}' | Reason: Invalid credentials")
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        elif not user.is_active:
            logger.warning(f"Login FAILED | Email: '{form_data.username}' | Reason: Inactive user")
            raise HTTPException(status_code=400, detail="Inactive user")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        logger.info(f"Login SUCCESS | Email: '{user.email}' | User ID: {user.id}")
        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login CRASH | Email: '{form_data.username}' | Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
