from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="candidate")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())

    
    otp_code = Column(String(10), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)

    
    profile_picture = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)