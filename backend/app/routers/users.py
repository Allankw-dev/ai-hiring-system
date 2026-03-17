from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dep import get_db, get_current_user
from app.models.user import User
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["Users"])


class ProfileUpdateRequest(BaseModel):
    full_name: str
    email: EmailStr


@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
    }


@router.put("/me")
def update_my_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_user = db.query(User).filter(
        User.email == payload.email,
        User.id != current_user.id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use"
        )

    current_user.full_name = payload.full_name
    current_user.email = payload.email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role
        }
    }