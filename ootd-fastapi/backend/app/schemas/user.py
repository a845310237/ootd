"""User schemas for request and response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=6, max_length=72)

    def model_post_init(self, __context):
        """Validate password byte length after initialization."""
        if self.password:
            password_bytes = self.password.encode('utf-8')
            if len(password_bytes) > 72:
                raise ValueError("Password is too long (maximum 72 bytes)")


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema."""

    name: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    body_type: Optional[str] = None
    skin_tone: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""

    id: str
    height: Optional[int] = None
    weight: Optional[int] = None
    body_type: Optional[str] = None
    skin_tone: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token data schema."""

    email: Optional[str] = None
