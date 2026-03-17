from datetime import datetime, timedelta, timezone
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.dep import get_db
from app.core.security import hash_password
from app.models.user import User
from app.services.email_service import send_reset_email

router = APIRouter(prefix="/password", tags=["Password Reset"])


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@router.post("/forgot")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if user:
        token = secrets.token_urlsafe(32)
        expiry = datetime.now(timezone.utc) + timedelta(hours=1)

        user.reset_token = token
        user.reset_token_expiry = expiry
        db.commit()

        reset_link = f"http://localhost:8501/?reset_token={token}"
        send_reset_email(user.email, reset_link)

    return {
        "message": "If an account with that email exists, a reset link has been sent."
    }


@router.post("/reset")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == payload.token).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    expiry = user.reset_token_expiry

    if expiry is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token expired or invalid"
        )

    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    user.password_hash = hash_password(payload.new_password)
    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()

    return {"message": "Password reset successfully"}