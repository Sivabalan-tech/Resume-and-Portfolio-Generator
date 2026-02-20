"""
Pydantic schemas for authentication — request/response validation.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from models.user import UserRole


# ─── Request Schemas ──────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.user


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─── Response Schemas ─────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    full_name: Optional[str] = None
    user_id: int


class UserPublic(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole

    class Config:
        from_attributes = True
