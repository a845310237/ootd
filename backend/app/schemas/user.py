"""User schemas for request and response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    name: Optional[str] = None
    height: Optional[int] = Field(None, ge=50, le=300, description="Height in centimeters")
    weight: Optional[int] = Field(None, ge=20, le=300, description="Weight in kilograms")
    body_type: Optional[str] = Field(None, max_length=50)
    skin_tone: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = Field(None, max_length=500)


class UserResponse(UserBase):
    """Schema for user response."""

    id: str
    height: Optional[int] = None
    weight: Optional[int] = None
    body_type: Optional[str] = None
    skin_tone: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserProfileResponse(UserResponse):
    """Extended user profile response."""

    pass
