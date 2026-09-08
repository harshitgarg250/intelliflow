"""
User-related Pydantic schemas
Request और response की shape define करते हैं यहाँ
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# ============== REQUEST SCHEMAS ==============
# जो user API को भेजता है


class UserCreate(BaseModel):
    """
    नया user register करते समय
    Frontend इस format में request भेजेगा
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        example = {
            "username": "harshit",
            "email": "harshit@example.com",
            "password": "SecurePass123!"
        }


class UserLogin(BaseModel):
    """
    Login करते समय
    सिर्फ email और password चाहिए
    """
    email: EmailStr
    password: str


# ============== RESPONSE SCHEMAS ==============
# जो API user को return करता है


class UserResponse(BaseModel):
    """
    User की information return करते समय
    Password को expose नहीं करेंगे (security के लिए)
    """
    id: UUID
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    Login/Register के बाद response
    Frontend को यह tokens मिलेंगे
    """
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse