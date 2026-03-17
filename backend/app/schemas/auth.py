from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminOTPVerifyRequest(BaseModel):
    email: EmailStr
    otp_code: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str