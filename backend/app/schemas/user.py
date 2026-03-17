from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True