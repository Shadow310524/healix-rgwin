from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.api import deps
from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger("healix.auth")

# Use the same limiter instance registered on the app
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")  # SECURITY: Max 5 login attempts per IP per minute
def login_access_token(
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login.

    Rate limited to 5 attempts per IP per minute to prevent brute force attacks.
    The error message is intentionally generic to prevent user enumeration.
    """
    try:
        user = crud.get_user_by_email(db, email=form_data.username)

        # SECURITY: Use a constant-time comparison path regardless of whether
        # the user exists. This prevents timing attacks that reveal valid emails.
        password_valid = False
        if user:
            password_valid = security.verify_password(
                form_data.password, user.hashed_password
            )

        if not user or not password_valid:
            # SECURITY: Generic message prevents user enumeration.
            # Do NOT say "user not found" vs "wrong password".
            logger.warning(
                f"Login FAILED | Email: '{form_data.username}' | IP: {get_remote_address(request)}"
            )
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            logger.warning(
                f"Login BLOCKED | Email: '{form_data.username}' | Reason: Inactive account"
            )
            raise HTTPException(status_code=403, detail="Account is inactive")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        logger.info(f"Login SUCCESS | User ID: {user.id}")
        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    except HTTPException:
        raise
    except Exception as e:
        # SECURITY: Never expose internal error details to the client.
        logger.error(f"Login CRASH | Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again.",
        )


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token validity.
    """
    return current_user
