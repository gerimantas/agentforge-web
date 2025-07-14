"""
User schemas for API validation

Pydantic models for user-related API requests and responses.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr

class UserCreate(UserBase):
    """Schema for user creation"""
    password: str

class UserUpdate(UserBase):
    """Schema for user updates"""
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    """Base schema for user in database"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """User schema for responses"""
    pass

class UserInDB(UserInDBBase):
    """User schema with hashed password"""
    hashed_password: str

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
